from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from app.services.news_service import NewsService, NewsServiceError


class MockGNewsResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload
        self.text = "ok"
        self.status_code = 200

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self._payload


class MockAsyncClient:
    def __init__(self, response: MockGNewsResponse, **_: object) -> None:
        self.response = response

    async def __aenter__(self) -> MockAsyncClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        return None

    async def get(self, *_: object, **__: object) -> MockGNewsResponse:
        return self.response


def article(url: str, title: str = "AI update") -> dict[str, object]:
    return {
        "title": title,
        "description": "Description",
        "source": {"name": "Source"},
        "url": url,
        "publishedAt": "2026-06-18T00:00:00Z",
    }


@pytest.mark.asyncio
async def test_search_news_deduplicates_articles_by_url() -> None:
    payload = {
        "articles": [
            article("https://news.example.com/story"),
            article("https://news.example.com/story/", "Duplicate"),
            article("https://news.example.com/other", "Other"),
        ]
    }
    response = MockGNewsResponse(payload)

    with patch("app.services.news_service.get_settings") as get_settings, patch(
        "app.services.news_service.httpx.AsyncClient",
        lambda **kwargs: MockAsyncClient(response, **kwargs),
    ):
        get_settings.return_value.gnews_api_key = "test-key"
        result = await NewsService().search_news("AI")

    assert [str(item.url).rstrip("/") for item in result.articles] == [
        "https://news.example.com/story",
        "https://news.example.com/other",
    ]


@pytest.mark.asyncio
async def test_search_news_empty_result_raises() -> None:
    response = MockGNewsResponse({"articles": []})

    with patch("app.services.news_service.get_settings") as get_settings, patch(
        "app.services.news_service.httpx.AsyncClient",
        lambda **kwargs: MockAsyncClient(response, **kwargs),
    ):
        get_settings.return_value.gnews_api_key = "test-key"
        with pytest.raises(NewsServiceError, match="No news articles"):
            await NewsService().search_news("missing topic")
