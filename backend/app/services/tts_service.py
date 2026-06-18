from __future__ import annotations

import asyncio
import re
from collections.abc import Sequence
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal, TypedDict, cast

import edge_tts

from app.config.settings import get_settings
from app.models.tts import TextToSpeechRequest, TextToSpeechResponse
from app.services.audio_service import AudioService, AudioServiceError


class TextToSpeechServiceError(Exception):
    pass


EDGE_TTS_TIMEOUT_SECONDS = 45
EDGE_TTS_MAX_ATTEMPTS = 2


class DialogueTurn(TypedDict):
    speaker: Literal["HOST_A", "HOST_B"]
    text: str


class TextToSpeechService:
    def __init__(self, audio_service: AudioService | None = None) -> None:
        self.settings = get_settings()
        self.audio_service = audio_service or AudioService()

    async def generate_podcast_audio(
        self,
        conversation: TextToSpeechRequest | Sequence[DialogueTurn],
        output_path: Path | None = None,
    ) -> TextToSpeechResponse:
        speaker_voices = self._resolve_speaker_voices()
        segments = self._resolve_segments(conversation)
        if not segments:
            raise TextToSpeechServiceError("No transcript segments were found")

        resolved_output_path = self._resolve_output_path(conversation, output_path)

        with TemporaryDirectory() as temp_dir:
            segment_files: list[Path] = []
            try:
                async def _synthesize_one(index: int, segment: DialogueTurn) -> Path:
                    voice = speaker_voices.get(segment["speaker"])
                    if not voice:
                        raise TextToSpeechServiceError(f"No voice configured for speaker {segment['speaker']}")

                    segment_path = Path(temp_dir) / f"segment_{index}.mp3"
                    await self._synthesize_segment(
                        text=segment["text"],
                        voice=voice,
                        output_path=segment_path,
                    )
                    return segment_path

                segment_files = list(
                    await asyncio.gather(
                        *[_synthesize_one(index, segment) for index, segment in enumerate(segments, start=1)]
                    )
                )

                await self.audio_service.merge_mp3_segments(segment_files, resolved_output_path)
            except AudioServiceError as exc:
                raise TextToSpeechServiceError(str(exc)) from exc
            finally:
                for segment_file in segment_files:
                    segment_file.unlink(missing_ok=True)

        return TextToSpeechResponse(
            output_filename=resolved_output_path.name,
            output_path=str(resolved_output_path.resolve()),
            segment_count=len(segments),
            speaker_voices=speaker_voices,
        )

    def _resolve_speaker_voices(self) -> dict[str, str]:
        if not self.settings.edge_tts_voice_a or not self.settings.edge_tts_voice_b:
            raise TextToSpeechServiceError("EDGE_TTS_VOICE_A and EDGE_TTS_VOICE_B must be configured")

        return {
            "HOST_A": self.settings.edge_tts_voice_a,
            "HOST_B": self.settings.edge_tts_voice_b,
        }

    @staticmethod
    def _resolve_segments(conversation: TextToSpeechRequest | Sequence[DialogueTurn]) -> list[DialogueTurn]:
        if isinstance(conversation, TextToSpeechRequest):
            return TextToSpeechService._split_transcript_into_segments(conversation.podcast_transcript)

        return TextToSpeechService._normalize_dialogue(conversation)

    @staticmethod
    def _resolve_output_path(
        conversation: TextToSpeechRequest | Sequence[DialogueTurn],
        output_path: Path | None,
    ) -> Path:
        if output_path is not None:
            resolved_output_path = output_path
        elif isinstance(conversation, TextToSpeechRequest):
            resolved_output_path = Path(conversation.output_filename)
        else:
            raise TextToSpeechServiceError("output_path is required when generating audio from dialogue turns")

        if resolved_output_path.suffix.lower() != ".mp3":
            resolved_output_path = resolved_output_path.with_suffix(".mp3")
        return resolved_output_path

    @staticmethod
    def _normalize_dialogue(conversation: Sequence[DialogueTurn]) -> list[DialogueTurn]:
        segments: list[DialogueTurn] = []
        for turn in conversation:
            speaker = turn.get("speaker")
            text = turn.get("text")
            if speaker not in {"HOST_A", "HOST_B"}:
                raise TextToSpeechServiceError(f"Unsupported speaker: {speaker}")
            if not isinstance(text, str) or not text.strip():
                raise TextToSpeechServiceError("Dialogue turn text cannot be empty")

            segments.append(
                {
                    "speaker": cast(Literal["HOST_A", "HOST_B"], speaker),
                    "text": re.sub(r"\s+", " ", text).strip(),
                }
            )

        return segments

    @staticmethod
    def _split_transcript_into_segments(transcript: str) -> list[DialogueTurn]:
        matches = list(re.finditer(r"(HOST_A|HOST_B):", transcript))
        if not matches:
            return []

        segments: list[DialogueTurn] = []
        for index, match in enumerate(matches):
            speaker = cast(Literal["HOST_A", "HOST_B"], match.group(1))
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(transcript)
            text = transcript[start:end].strip()
            if text:
                segments.append({"speaker": speaker, "text": re.sub(r"\s+", " ", text).strip()})

        return segments

    @staticmethod
    async def _synthesize_segment(text: str, voice: str, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        last_error: Exception | None = None
        for attempt in range(1, EDGE_TTS_MAX_ATTEMPTS + 1):
            try:
                communicate = edge_tts.Communicate(text=text, voice=voice)
                await asyncio.wait_for(communicate.save(str(output_path)), timeout=EDGE_TTS_TIMEOUT_SECONDS)
                return
            except Exception as exc:  # pragma: no cover - external service failure handling
                last_error = exc
                if attempt < EDGE_TTS_MAX_ATTEMPTS:
                    await asyncio.sleep(0.75 * attempt)

        raise TextToSpeechServiceError(f"Failed to synthesize Edge TTS audio segment: {last_error}") from last_error

    async def _merge_mp3_segments(self, segment_files: list[Path], output_path: Path) -> None:
        try:
            await self.audio_service.merge_mp3_segments(segment_files, output_path)
        except AudioServiceError as exc:
            raise TextToSpeechServiceError(f"Failed to merge MP3 segments: {exc}") from exc
