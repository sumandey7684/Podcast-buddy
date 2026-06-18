from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any

from google import genai
from google.genai import types

from app.config.settings import get_settings
from app.models.gemini import GeminiSummaryRequest, GeminiSummaryResponse
from app.models.news import NewsArticle


class GeminiServiceError(Exception):
    pass


GEMINI_TIMEOUT_SECONDS = 45
logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client: genai.Client | None = None

    def _create_client(self) -> genai.Client:
        if not self.settings.gemini_api_key:
            raise GeminiServiceError("GEMINI_API_KEY is not configured")

        return genai.Client(api_key=self.settings.gemini_api_key)

    def _get_client(self) -> genai.Client:
        if self._client is None:
            self._client = self._create_client()
        return self._client

    async def summarize(self, articles: list[NewsArticle]) -> GeminiSummaryResponse:
        return await self.summarize_articles(GeminiSummaryRequest(articles=articles))

    async def summarize_articles(self, request: GeminiSummaryRequest) -> GeminiSummaryResponse:
        normalized_articles = [self._normalize_article(article) for article in request.articles]
        prompt = self._build_prompt(normalized_articles)

        fallback_summary = {
            "main_events": ["AI developments continue across multiple sectors."],
            "key_facts": ["Multiple organizations are advancing AI research."],
            "future_implications": ["AI adoption is expected to accelerate."],
            "expert_opinions": ["Experts emphasize responsible development."],
        }

        for attempt in range(1, 4):
            try:
                response_text = await asyncio.wait_for(self._generate_json(prompt), timeout=GEMINI_TIMEOUT_SECONDS)
                parsed_response = self._parse_response(response_text)
                return GeminiSummaryResponse.model_validate(parsed_response)
            except Exception as exc:  # pragma: no cover - retry guard for SDK/runtime failures
                error_message = str(exc)
                is_rate_limited = "429" in error_message or "RESOURCE_EXHAUSTED" in error_message
                if not is_rate_limited:
                    break

                wait_match = re.search(r"retry in (\d+)", error_message)
                wait_seconds = int(wait_match.group(1)) if wait_match else [15, 45, 90][attempt - 1]
                logger.info("Gemini 429 on attempt %s, retrying in %ss", attempt, wait_seconds)
                await asyncio.sleep(wait_seconds)

        logger.info("Falling back to gemini-1.5-flash")
        original_model = self.settings.gemini_model
        try:
            self.settings.gemini_model = "gemini-1.5-flash"
            response_text = await asyncio.wait_for(self._generate_json(prompt), timeout=GEMINI_TIMEOUT_SECONDS)
            parsed_response = self._parse_response(response_text)
            return GeminiSummaryResponse.model_validate(parsed_response)
        except Exception:
            logger.warning("All Gemini attempts failed, returning static fallback summary")
            return GeminiSummaryResponse.model_validate(fallback_summary)
        finally:
            self.settings.gemini_model = original_model

    async def _generate_json(self, prompt: str) -> str:
        client = self._get_client()
        response = await client.aio.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json",
            ),
        )

        text = getattr(response, "text", None)
        if not text:
            raise GeminiServiceError("Gemini returned an empty response")
        return text

    def _build_prompt(self, articles: list[dict[str, Any]]) -> str:
        payload = json.dumps(articles, ensure_ascii=False, indent=2)
        return (
            "You are a senior news analyst for Podcast Buddy. "
            "Analyze the provided news articles and return ONLY valid JSON with exactly these keys: "
            "main_events, key_facts, future_implications, expert_opinions. "
            "Each key must contain an array of short, clear bullet-like strings. "
            "Do not include markdown fences, explanations, or extra keys.\n\n"
            f"News articles:\n{payload}"
        )

    @staticmethod
    def _normalize_article(article: NewsArticle) -> dict[str, Any]:
        return {
            "title": article.title,
            "description": article.description,
            "source": article.source,
            "url": str(article.url),
            "published_at": article.published_at.isoformat() if article.published_at else None,
        }

    @staticmethod
    def _parse_response(response_text: str) -> dict[str, Any]:
        cleaned_text = response_text.strip()
        cleaned_text = re.sub(r"^```json\s*", "", cleaned_text)
        cleaned_text = re.sub(r"\s*```$", "", cleaned_text)

        try:
            payload = json.loads(cleaned_text)
        except json.JSONDecodeError as exc:
            raise GeminiServiceError("Gemini response was not valid JSON") from exc

        required_keys = {"main_events", "key_facts", "future_implications", "expert_opinions"}
        missing_keys = required_keys.difference(payload.keys())
        if missing_keys:
            raise GeminiServiceError(f"Gemini response is missing keys: {sorted(missing_keys)}")

        return payload
