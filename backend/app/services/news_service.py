from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

import httpx

from app.config.settings import get_settings
from app.models.news import NewsArticle, NewsSearchRequest, NewsSearchResponse


class NewsServiceError(Exception):
    pass


GNEWS_TIMEOUT_SECONDS = 15.0
GNEWS_MAX_ATTEMPTS = 3


class NewsService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://gnews.io/api/v4/search"

    async def search_news(
        self,
        topic: NewsSearchRequest | str,
        limit: int | None = None,
        language: str = "en",
    ) -> NewsSearchResponse:
        if not self.settings.gnews_api_key:
            raise NewsServiceError("GNEWS_API_KEY is not configured")

        if isinstance(topic, NewsSearchRequest):
            request = topic
        else:
            request = NewsSearchRequest(topic=topic, limit=limit or 10, language=language)

        params = {
            "q": request.topic,
            "lang": request.language,
            "max": request.limit,
            "token": self.settings.gnews_api_key,
        }

        payload = await self._request_with_retries(params)

        articles = self._deduplicate_articles_by_url(
            [self._parse_article(article) for article in payload.get("articles", [])]
        )
        if not articles:
            raise NewsServiceError(f"No news articles were found for topic: {request.topic}")

        return NewsSearchResponse(
            topic=request.topic,
            total_results=len(articles),
            articles=articles,
        )

    @staticmethod
    def _deduplicate_articles_by_url(articles: list[NewsArticle]) -> list[NewsArticle]:
        deduplicated: list[NewsArticle] = []
        seen_urls: set[str] = set()

        for article in articles:
            url = str(article.url).rstrip("/").lower()
            if url in seen_urls:
                continue
            seen_urls.add(url)
            deduplicated.append(article)

        return deduplicated

    async def _request_with_retries(self, params: dict[str, Any]) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(1, GNEWS_MAX_ATTEMPTS + 1):
            try:
                async with httpx.AsyncClient(timeout=GNEWS_TIMEOUT_SECONDS) as client:
                    response = await client.get(self.base_url, params=params)
                    response.raise_for_status()
                    payload: dict[str, Any] = response.json()
                    return payload
            except httpx.HTTPStatusError as exc:
                last_error = exc
                if exc.response.status_code < 500:
                    detail = exc.response.text or str(exc)
                    raise NewsServiceError(f"GNews request failed: {detail}") from exc
            except httpx.RequestError as exc:
                last_error = exc
            except ValueError as exc:
                raise NewsServiceError("Invalid JSON received from GNews") from exc

            if attempt < GNEWS_MAX_ATTEMPTS:
                await asyncio.sleep(0.75 * attempt)

        raise NewsServiceError(f"Unable to reach GNews after {GNEWS_MAX_ATTEMPTS} attempts: {last_error}") from last_error

    def _parse_article(self, article: dict[str, Any]) -> NewsArticle:
        source_value = article.get("source") or {}
        source_name = source_value.get("name") if isinstance(source_value, dict) else None

        published_at = self._parse_datetime(article.get("publishedAt"))

        return NewsArticle(
            title=article.get("title") or "Untitled article",
            description=article.get("description"),
            source=source_name or "Unknown source",
            url=article["url"],
            published_at=published_at,
        )

    @staticmethod
    def _parse_datetime(value: Any) -> datetime | None:
        if not value or not isinstance(value, str):
            return None

        normalized_value = value.replace("Z", "+00:00")
        try:
            parsed_value = datetime.fromisoformat(normalized_value)
        except ValueError:
            return None

        if parsed_value.tzinfo is None:
            return parsed_value.replace(tzinfo=timezone.utc)
        return parsed_value