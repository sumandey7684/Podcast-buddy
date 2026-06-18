from __future__ import annotations

import json
import shutil
import tempfile
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Protocol, TypedDict, cast
from uuid import uuid4

import edge_tts

from app.config.settings import get_settings
from app.models.gemini import GeminiSummaryResponse
from app.models.news import NewsArticle, NewsSearchResponse
from app.models.podcast import (
    PodcastGenerateRequest,
    PodcastGenerateResponse,
    PodcastMetadata,
    PodcastSource,
    PodcastTranscript,
)
from app.services.audio_service import AudioService, AudioServiceError
from app.services.gemini_service import GeminiService, GeminiServiceError
from app.services.news_service import NewsService, NewsServiceError
from app.services.script_service import ScriptService, ScriptServiceError
from app.utils.text import clean_text


DEFAULT_AUDIO_DIR = Path(__file__).resolve().parents[2] / "static" / "audio"
SUMMARY_KEYS = {"main_events", "key_facts", "future_implications", "expert_opinions"}
SPEAKERS = {"HOST_A", "HOST_B"}
VOICE_BY_SPEAKER = {
    "HOST_A": "en-US-AndrewNeural",
    "HOST_B": "en-US-EmmaNeural",
}
EDGE_TTS_TIMEOUT_SECONDS = 45
EDGE_TTS_MAX_ATTEMPTS = 2


class DialogueTurn(TypedDict):
    speaker: Literal["HOST_A", "HOST_B"]
    text: str


class NewsPipelineService(Protocol):
    async def search_news(self, topic: str, limit: int, language: str = "en") -> NewsSearchResponse:
        ...


class GeminiPipelineService(Protocol):
    async def summarize(self, articles: list[NewsArticle]) -> GeminiSummaryResponse:
        ...


class ScriptPipelineService(Protocol):
    async def generate_dialogue(
        self,
        topic: str,
        summary: GeminiSummaryResponse | dict[str, list[str]],
    ) -> list[DialogueTurn]:
        ...


class PodcastServiceError(Exception):
    pass


class PodcastBadRequestError(ValueError):
    pass


class PodcastExternalServiceError(PodcastServiceError):
    pass


class PodcastService:
    def __init__(
        self,
        news_service: NewsPipelineService | None = None,
        gemini_service: GeminiPipelineService | None = None,
        script_service: ScriptPipelineService | None = None,
        audio_service: AudioService | None = None,
        audio_dir: Path = DEFAULT_AUDIO_DIR,
    ) -> None:
        self.settings = get_settings()
        self.news_service = news_service or NewsService()
        self.gemini_service = gemini_service or GeminiService()
        self.script_service = script_service or ScriptService()
        self.audio_service = audio_service or AudioService()
        self.audio_dir = audio_dir

    async def generate(self, topic: str | PodcastGenerateRequest) -> PodcastGenerateResponse:
        topic_text = self._resolve_topic(topic)
        request_id = uuid4().hex
        temp_dir = Path(tempfile.mkdtemp(prefix=f"podcast_{request_id}_"))
        segment_paths: list[Path] = []

        try:
            articles = await self._get_deduplicated_articles(topic_text)
            summary_payload = await self._summarize_articles(articles)
            dialogue = await self._generate_dialogue(topic_text, summary_payload)

            output_path = self.audio_dir / f"episode_{request_id}.mp3"
            segment_paths = await self._generate_audio_segments(dialogue, temp_dir)
            await self._merge_audio_segments(segment_paths, output_path)

            return PodcastGenerateResponse(
                request_id=request_id,
                topic=topic_text,
                sources=[self._article_to_source(article) for article in articles],
                summary=self._format_summary(summary_payload),
                transcript=self._build_transcript(dialogue),
                audio_url=f"/static/audio/episode_{request_id}.mp3",
                metadata=PodcastMetadata(
                    article_count=len(articles),
                    generated_at=datetime.now(timezone.utc),
                    provider_name=self.settings.default_news_provider,
                ),
            )
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    @staticmethod
    def _resolve_topic(topic: str | PodcastGenerateRequest) -> str:
        if isinstance(topic, PodcastGenerateRequest):
            topic_text = topic.topic
        else:
            topic_text = topic

        topic_text = topic_text.strip()
        if not topic_text:
            raise PodcastBadRequestError("Topic is required")
        return topic_text

    async def _get_deduplicated_articles(self, topic: str) -> list[NewsArticle]:
        try:
            news_response = await self.news_service.search_news(topic)
        except NewsServiceError:
            raise
        except Exception as exc:
            raise PodcastExternalServiceError(f"Unexpected news service failure: {exc}") from exc

        articles = self._deduplicate_articles_by_url(news_response.articles)
        if not articles:
            raise PodcastExternalServiceError(f"No news articles were found for topic: {topic}")

        return articles

    async def _summarize_articles(self, articles: list[NewsArticle]) -> dict[str, list[str]]:
        try:
            summary = await self.gemini_service.summarize(articles)
        except GeminiServiceError:
            raise
        except Exception as exc:
            raise PodcastExternalServiceError(f"Unexpected Gemini service failure: {exc}") from exc

        summary_payload = self._summary_to_dict(summary)
        missing_keys = SUMMARY_KEYS.difference(summary_payload.keys())
        if missing_keys:
            raise PodcastExternalServiceError(f"Gemini summary is missing keys: {sorted(missing_keys)}")

        return summary_payload

    async def _generate_dialogue(self, topic: str, summary: dict[str, list[str]]) -> list[DialogueTurn]:
        try:
            dialogue = await self.script_service.generate_dialogue(topic=topic, summary=summary)
        except ScriptServiceError:
            raise
        except Exception as exc:
            raise PodcastExternalServiceError(f"Unexpected script service failure: {exc}") from exc

        return self._validate_dialogue(dialogue)

    async def _generate_audio_segments(self, dialogue: list[DialogueTurn], temp_dir: Path) -> list[Path]:
        segment_paths: list[Path] = []
        for index, turn in enumerate(dialogue):
            speaker = turn["speaker"]
            voice = VOICE_BY_SPEAKER[speaker]
            segment_path = temp_dir / f"segment_{index}.mp3"
            await self._save_edge_tts_segment(
                text=turn["text"],
                voice=voice,
                segment_path=segment_path,
                index=index,
                speaker=speaker,
            )

            if not segment_path.exists():
                raise PodcastExternalServiceError(f"Edge TTS did not create segment {index}")

            segment_paths.append(segment_path)

        return segment_paths

    async def _merge_audio_segments(self, segment_paths: list[Path], output_path: Path) -> None:
        try:
            await self.audio_service.merge_mp3_segments(segment_paths, output_path)
        except AudioServiceError:
            raise
        except Exception as exc:
            raise PodcastExternalServiceError(f"Unexpected audio merge failure: {exc}") from exc

    @staticmethod
    async def _save_edge_tts_segment(
        text: str,
        voice: str,
        segment_path: Path,
        index: int,
        speaker: str,
    ) -> None:
        last_error: Exception | None = None
        for attempt in range(1, EDGE_TTS_MAX_ATTEMPTS + 1):
            try:
                communicate = edge_tts.Communicate(text=text, voice=voice)
                await asyncio.wait_for(communicate.save(str(segment_path)), timeout=EDGE_TTS_TIMEOUT_SECONDS)
                return
            except Exception as exc:
                last_error = exc
                if attempt >= EDGE_TTS_MAX_ATTEMPTS:
                    break
                await asyncio.sleep(0.75 * attempt)

        raise PodcastExternalServiceError(
            f"Failed to generate TTS segment {index} for {speaker}: {last_error}"
        ) from last_error

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

    @staticmethod
    def _summary_to_dict(summary: GeminiSummaryResponse | dict[str, Any]) -> dict[str, list[str]]:
        if isinstance(summary, GeminiSummaryResponse):
            raw_summary: dict[str, Any] = summary.model_dump()
        elif isinstance(summary, dict):
            raw_summary = summary
        else:
            raise PodcastExternalServiceError("Gemini summary has an unsupported format")

        summary_payload: dict[str, list[str]] = {}
        for key in SUMMARY_KEYS:
            value = raw_summary.get(key)
            if not isinstance(value, list):
                continue
            summary_payload[key] = [clean_text(str(item)) for item in value if str(item).strip()]

        return summary_payload

    @staticmethod
    def _validate_dialogue(dialogue: Any) -> list[DialogueTurn]:
        if not isinstance(dialogue, list) or not dialogue:
            raise PodcastExternalServiceError("Script dialogue cannot be empty")
        if len(dialogue) < 6:
            raise PodcastExternalServiceError("Script dialogue must contain at least 6 turns")

        validated_dialogue: list[DialogueTurn] = []
        for index, turn in enumerate(dialogue):
            if not isinstance(turn, dict):
                raise PodcastExternalServiceError(f"Dialogue turn {index} must be an object")

            speaker = turn.get("speaker")
            text = turn.get("text")
            if speaker not in SPEAKERS:
                raise PodcastExternalServiceError(f"Invalid dialogue speaker at turn {index}: {speaker}")
            if not isinstance(text, str) or not text.strip():
                raise PodcastExternalServiceError(f"Dialogue text is required at turn {index}")

            validated_dialogue.append(
                {
                    "speaker": cast(Literal["HOST_A", "HOST_B"], speaker),
                    "text": clean_text(text),
                }
            )

        return validated_dialogue

    @staticmethod
    def _format_summary(summary: dict[str, list[str]]) -> str:
        return json.dumps(summary, ensure_ascii=False)

    @staticmethod
    def _build_transcript(dialogue: list[DialogueTurn]) -> PodcastTranscript:
        host_a_lines = [turn["text"] for turn in dialogue if turn["speaker"] == "HOST_A"]
        host_b_lines = [turn["text"] for turn in dialogue if turn["speaker"] == "HOST_B"]
        full_script = "\n\n".join(f"{turn['speaker']}: {turn['text']}" for turn in dialogue)

        return PodcastTranscript(
            host_a=" ".join(host_a_lines),
            host_b=" ".join(host_b_lines),
            full_script=full_script,
        )

    @staticmethod
    def _article_to_source(article: NewsArticle) -> PodcastSource:
        return PodcastSource(
            title=article.title,
            url=article.url,
            source_name=article.source,
            published_at=article.published_at or datetime.now(timezone.utc),
            snippet=article.description or article.title,
        )

