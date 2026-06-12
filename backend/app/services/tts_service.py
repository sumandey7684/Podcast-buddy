from __future__ import annotations

import asyncio
import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory

from elevenlabs.client import AsyncElevenLabs

from app.config.settings import get_settings
from app.models.tts import TextToSpeechRequest, TextToSpeechResponse


class TextToSpeechServiceError(Exception):
    pass


class TextToSpeechService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._client: AsyncElevenLabs | None = None

    def _create_client(self) -> AsyncElevenLabs:
        if not self.settings.elevenlabs_api_key:
            raise TextToSpeechServiceError("ELEVENLABS_API_KEY is not configured")

        return AsyncElevenLabs(api_key=self.settings.elevenlabs_api_key)

    def _get_client(self) -> AsyncElevenLabs:
        if self._client is None:
            self._client = self._create_client()
        return self._client

    async def generate_podcast_audio(self, request: TextToSpeechRequest) -> TextToSpeechResponse:
        speaker_voices = self._resolve_speaker_voices()
        segments = self._split_transcript_into_segments(request.podcast_transcript)
        if not segments:
            raise TextToSpeechServiceError("No transcript segments were found")

        output_path = Path(request.output_filename)
        if output_path.suffix.lower() != ".mp3":
            output_path = output_path.with_suffix(".mp3")

        with TemporaryDirectory() as temp_dir:
            segment_files: list[Path] = []
            try:
                for index, segment in enumerate(segments, start=1):
                    voice_id = speaker_voices.get(segment["speaker"])
                    if not voice_id:
                        raise TextToSpeechServiceError(f"No voice configured for speaker {segment['speaker']}")

                    segment_path = Path(temp_dir) / f"segment_{index}.mp3"
                    await self._synthesize_segment(
                        text=segment["text"],
                        voice_id=voice_id,
                        output_path=segment_path,
                    )
                    segment_files.append(segment_path)

                await self._merge_mp3_segments(segment_files, output_path)
            finally:
                for segment_file in segment_files:
                    if segment_file.exists():
                        segment_file.unlink(missing_ok=True)

        return TextToSpeechResponse(
            output_filename=output_path.name,
            output_path=str(output_path.resolve()),
            segment_count=len(segments),
            speaker_voices=speaker_voices,
        )

    def _resolve_speaker_voices(self) -> dict[str, str]:
        if not self.settings.elevenlabs_voice_a_id or not self.settings.elevenlabs_voice_b_id:
            raise TextToSpeechServiceError("ELEVENLABS_VOICE_A_ID and ELEVENLABS_VOICE_B_ID must be configured")

        return {
            "HOST_A": self.settings.elevenlabs_voice_a_id,
            "HOST_B": self.settings.elevenlabs_voice_b_id,
        }

    @staticmethod
    def _split_transcript_into_segments(transcript: str) -> list[dict[str, str]]:
        matches = list(re.finditer(r"(HOST_A|HOST_B):", transcript))
        if not matches:
            return []

        segments: list[dict[str, str]] = []
        for index, match in enumerate(matches):
            speaker = match.group(1)
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(transcript)
            text = transcript[start:end].strip()
            if text:
                segments.append({"speaker": speaker, "text": text})

        return segments

    async def _synthesize_segment(self, text: str, voice_id: str, output_path: Path) -> None:
        client = self._get_client()
        try:
            audio_stream = await client.text_to_speech.convert(
                voice_id=voice_id,
                model_id=self.settings.elevenlabs_model_id,
                text=text,
                output_format="mp3_44100_128",
            )
            await self._write_stream_to_file(audio_stream, output_path)
        except Exception as exc:  # pragma: no cover - external API failure handling
            raise TextToSpeechServiceError(f"Failed to synthesize audio segment: {exc}") from exc

    @staticmethod
    async def _write_stream_to_file(audio_stream: object, output_path: Path) -> None:
        if hasattr(audio_stream, "read"):
            audio_bytes = await audio_stream.read()
        else:
            audio_bytes = audio_stream

        if not isinstance(audio_bytes, (bytes, bytearray)):
            raise TextToSpeechServiceError("ElevenLabs returned an invalid audio payload")

        output_path.write_bytes(audio_bytes)

    async def _merge_mp3_segments(self, segment_files: list[Path], output_path: Path) -> None:
        loop = asyncio.get_running_loop()

        def _concat_files() -> None:
            with output_path.open("wb") as destination:
                for segment_file in segment_files:
                    destination.write(segment_file.read_bytes())

        try:
            await loop.run_in_executor(None, _concat_files)
        except Exception as exc:  # pragma: no cover - filesystem failure handling
            raise TextToSpeechServiceError(f"Failed to merge MP3 segments: {exc}") from exc
