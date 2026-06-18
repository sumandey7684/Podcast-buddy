from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from app.models.gemini import GeminiSummaryResponse
from app.models.news import NewsArticle, NewsSearchResponse
from app.models.podcast import PodcastGenerateResponse
from app.services.podcast_service import PodcastService


class FakeNewsService:
    async def search_news(self, topic: str, limit: int = 10, language: str = "en") -> NewsSearchResponse:
        published_at = datetime(2026, 6, 18, tzinfo=timezone.utc)
        return NewsSearchResponse(
            topic=topic,
            total_results=2,
            articles=[
                NewsArticle(
                    title="AI infrastructure expands",
                    description="New data centers are being built.",
                    source="Reuters",
                    url="https://www.reuters.com/technology/ai-infrastructure",
                    published_at=published_at,
                ),
                NewsArticle(
                    title="AI infrastructure expands duplicate",
                    description="Duplicate URL.",
                    source="Reuters",
                    url="https://www.reuters.com/technology/ai-infrastructure",
                    published_at=published_at,
                ),
            ],
        )


class FakeGeminiService:
    async def summarize(self, articles: list[NewsArticle]) -> GeminiSummaryResponse:
        return GeminiSummaryResponse(
            main_events=["AI infrastructure spending is growing."],
            key_facts=["Demand for compute is rising."],
            future_implications=["More data center capacity may be needed."],
            expert_opinions=["Analysts expect infrastructure constraints."],
        )


class FakeScriptService:
    async def generate_dialogue(self, topic: str, summary: dict[str, list[str]]) -> list[dict[str, str]]:
        return [
            {"speaker": "HOST_A", "text": f"Welcome to {topic}."},
            {"speaker": "HOST_B", "text": "That is a big story."},
            {"speaker": "HOST_A", "text": summary["main_events"][0]},
            {"speaker": "HOST_B", "text": summary["expert_opinions"][0]},
            {"speaker": "HOST_A", "text": summary["future_implications"][0]},
            {"speaker": "HOST_B", "text": "We will keep watching it."},
        ]


class FakeAudioService:
    async def merge_mp3_segments(self, segment_files: list[Path], output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(b"merged mp3")


class FakeCommunicate:
    def __init__(self, text: str, voice: str) -> None:
        self.text = text
        self.voice = voice

    async def save(self, output_path: str) -> None:
        Path(output_path).write_bytes(b"segment mp3")


@pytest.mark.asyncio
async def test_podcast_pipeline_response_contains_required_fields(tmp_path: Path) -> None:
    service = PodcastService(
        news_service=FakeNewsService(),
        gemini_service=FakeGeminiService(),
        script_service=FakeScriptService(),
        audio_service=FakeAudioService(),
        audio_dir=tmp_path,
    )

    with patch("app.services.podcast_service.edge_tts.Communicate", FakeCommunicate):
        response = await service.generate("AI infrastructure")

    assert isinstance(response, PodcastGenerateResponse)
    assert response.request_id
    assert response.topic == "AI infrastructure"
    assert len(response.sources) == 1
    assert response.summary
    assert response.transcript.full_script.startswith("HOST_A:")
    assert response.audio_url.startswith("/static/audio/")
    assert response.audio_url.endswith(f"episode_{response.request_id}.mp3")
    assert response.metadata.article_count == 1
    assert response.metadata.generated_at is not None
