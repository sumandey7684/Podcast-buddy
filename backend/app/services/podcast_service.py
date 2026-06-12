from datetime import datetime, timezone
from uuid import uuid4

from app.config.settings import get_settings
from app.models.podcast import (
    PodcastGenerateRequest,
    PodcastGenerateResponse,
    PodcastMetadata,
    PodcastSource,
    PodcastTranscript,
)
from app.utils.text import clean_text, merge_context


class PodcastService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def generate(self, request: PodcastGenerateRequest) -> PodcastGenerateResponse:
        topic = request.topic.strip()
        if not topic:
            raise ValueError("Topic is required")

        sources = self._build_sources(topic)
        context = merge_context([source.snippet for source in sources])
        summary = clean_text(
            f"Latest news digest for {topic}. "
            f"This MVP backend assembles articles into a compact context: {context}"
        )
        transcript = self._build_transcript(topic, summary)

        return PodcastGenerateResponse(
            request_id=str(uuid4()),
            topic=topic,
            sources=sources,
            summary=summary,
            transcript=transcript,
            audio_url=f"{self.settings.audio_base_url}/sample-audio.mp3",
            metadata=PodcastMetadata(
                article_count=len(sources),
                generated_at=datetime.now(timezone.utc),
                provider_name=self.settings.default_news_provider,
            ),
        )

    def _build_sources(self, topic: str) -> list[PodcastSource]:
        return [
            PodcastSource(
                title=f"{topic} update 1",
                url="https://example.com/article-1",
                source_name=self.settings.default_news_provider,
                published_at=datetime.now(timezone.utc),
                snippet=f"A concise news brief about {topic} from source one.",
            ),
            PodcastSource(
                title=f"{topic} update 2",
                url="https://example.com/article-2",
                source_name=self.settings.default_news_provider,
                published_at=datetime.now(timezone.utc),
                snippet=f"Another article adding context to {topic} from source two.",
            ),
        ]

    def _build_transcript(self, topic: str, summary: str) -> PodcastTranscript:
        host_a = f"Welcome back to Podcast Buddy. Today we are covering {topic}."
        host_b = f"Here is the quick summary: {summary}"
        host_a_reply = "We will keep following this story and bring you the main updates."
        full_script = "\n".join([f"Host A: {host_a}", f"Host B: {host_b}", f"Host A: {host_a_reply}"])

        return PodcastTranscript(
            host_a=host_a,
            host_b=host_b,
            full_script=full_script,
        )