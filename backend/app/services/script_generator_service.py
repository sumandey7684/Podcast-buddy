from __future__ import annotations

import asyncio
import json
import re
from typing import Any

from google import genai
from google.genai import types

from app.config.settings import get_settings
from app.models.script import PodcastScriptRequest, PodcastScriptResponse
from app.prompts.podcast_script_prompt import build_podcast_script_prompt


class ScriptGeneratorError(Exception):
    pass


class ScriptGeneratorService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client: genai.Client | None = None

    def _create_client(self) -> genai.Client:
        if not self.settings.gemini_api_key:
            raise ScriptGeneratorError("GEMINI_API_KEY is not configured")

        return genai.Client(api_key=self.settings.gemini_api_key)

    def _get_client(self) -> genai.Client:
        if self._client is None:
            self._client = self._create_client()
        return self._client

    async def generate_script(self, request: PodcastScriptRequest) -> PodcastScriptResponse:
        prompt = build_podcast_script_prompt(
            structured_summary=request.structured_summary,
            topic=request.topic,
            conversation_minutes=request.conversation_minutes,
        )

        last_error: Exception | None = None
        for attempt in range(1, self.settings.gemini_max_retries + 1):
            try:
                response_text = await self._generate_json(prompt)
                parsed_response = self._parse_response(response_text)
                return PodcastScriptResponse.model_validate(parsed_response)
            except Exception as exc:  # pragma: no cover - retry guard for SDK/runtime failures
                last_error = exc
                if attempt >= self.settings.gemini_max_retries:
                    break
                await asyncio.sleep(self.settings.gemini_retry_base_delay_seconds * attempt)

        raise ScriptGeneratorError(f"Podcast script generation failed: {last_error}") from last_error

    async def _generate_json(self, prompt: str) -> str:
        client = self._get_client()
        response = await client.aio.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                response_mime_type="application/json",
            ),
        )

        text = getattr(response, "text", None)
        if not text:
            raise ScriptGeneratorError("Gemini returned an empty response")
        return text

    @staticmethod
    def _parse_response(response_text: str) -> dict[str, Any]:
        cleaned_text = response_text.strip()
        cleaned_text = re.sub(r"^```json\s*", "", cleaned_text)
        cleaned_text = re.sub(r"\s*```$", "", cleaned_text)

        try:
            payload = json.loads(cleaned_text)
        except json.JSONDecodeError as exc:
            raise ScriptGeneratorError("Gemini response was not valid JSON") from exc

        required_keys = {"host_a", "host_b", "full_script", "estimated_duration_minutes"}
        missing_keys = required_keys.difference(payload.keys())
        if missing_keys:
            raise ScriptGeneratorError(f"Gemini response is missing keys: {sorted(missing_keys)}")

        return payload
