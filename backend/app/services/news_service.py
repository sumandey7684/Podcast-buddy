from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx

from app.config.settings import get_settings
from app.models.news import NewsArticle, NewsSearchRequest, NewsSearchResponse


class NewsServiceError(Exception):
    pass


class NewsService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://gnews.io/api/v4/search"

    async def search_news(self, request: NewsSearchRequest) -> NewsSearchResponse:
        if not self.settings.gnews_api_key:
            raise NewsServiceError("GNEWS_API_KEY is not configured")

        params = {
            "q": request.topic,
            "lang": request.language,
            "max": request.limit,
            "token": self.settings.gnews_api_key,
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                payload: dict[str, Any] = response.json()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text or str(exc)
            raise NewsServiceError(f"GNews request failed: {detail}") from exc
        except httpx.RequestError as exc:
            raise NewsServiceError(f"Unable to reach GNews: {exc}") from exc
        except ValueError as exc:
            raise NewsServiceError("Invalid JSON received from GNews") from exc

        articles = [self._parse_article(article) for article in payload.get("articles", [])]

        return NewsSearchResponse(
            topic=request.topic,
            total_results=len(articles),
            articles=articles,
        )

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