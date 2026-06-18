from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from app.services.tts_service import TextToSpeechService


class FakeAudioService:
    def __init__(self) -> None:
        self.segment_names: list[str] = []

    async def merge_mp3_segments(self, segment_files: list[Path], output_path: Path) -> None:
        self.segment_names = [segment.name for segment in segment_files]
        output_path.write_bytes(b"merged mp3")


class FakeCommunicate:
    calls: list[tuple[str, str, str]] = []

    def __init__(self, text: str, voice: str) -> None:
        self.text = text
        self.voice = voice

    async def save(self, output_path: str) -> None:
        FakeCommunicate.calls.append((self.text, self.voice, Path(output_path).name))
        Path(output_path).write_bytes(b"segment mp3")


@pytest.mark.asyncio
async def test_tts_generates_segment_files_and_maps_host_voices(tmp_path: Path) -> None:
    FakeCommunicate.calls = []
    audio_service = FakeAudioService()
    service = TextToSpeechService(audio_service=audio_service)
    output_path = tmp_path / "episode.mp3"

    with patch("app.services.tts_service.edge_tts.Communicate", FakeCommunicate):
        response = await service.generate_podcast_audio(
            conversation=[
                {"speaker": "HOST_A", "text": "Host A line."},
                {"speaker": "HOST_B", "text": "Host B line."},
            ],
            output_path=output_path,
        )

    assert FakeCommunicate.calls == [
        ("Host A line.", "en-US-AndrewNeural", "segment_1.mp3"),
        ("Host B line.", "en-US-EmmaNeural", "segment_2.mp3"),
    ]
    assert audio_service.segment_names == ["segment_1.mp3", "segment_2.mp3"]
    assert response.segment_count == 2
    assert output_path.read_bytes() == b"merged mp3"
