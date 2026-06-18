from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from app.services.audio_service import AudioService, AudioServiceError


class CompletedFFmpeg:
    def __init__(self, returncode: int = 0, stderr: str = "") -> None:
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = ""


@pytest.mark.asyncio
async def test_merge_uses_unique_concat_file_and_deletes_it(tmp_path: Path) -> None:
    segment_a = tmp_path / "a.mp3"
    segment_b = tmp_path / "b.mp3"
    output_a = tmp_path / "episode_a.mp3"
    output_b = tmp_path / "episode_b.mp3"
    segment_a.write_bytes(b"a")
    segment_b.write_bytes(b"b")
    concat_files: list[Path] = []

    def fake_run(command: list[str], **_: object) -> CompletedFFmpeg:
        concat_path = Path(command[command.index("-i") + 1])
        concat_files.append(concat_path)
        Path(command[-1]).write_bytes(b"merged")
        return CompletedFFmpeg()

    with patch("app.services.audio_service.subprocess.run", side_effect=fake_run):
        await AudioService().merge_mp3_segments([segment_a, segment_b], output_a)
        await AudioService().merge_mp3_segments([segment_a, segment_b], output_b)

    assert len(concat_files) == 2
    assert concat_files[0].name.startswith("concat_")
    assert concat_files[1].name.startswith("concat_")
    assert concat_files[0] != concat_files[1]
    assert all(not concat_file.exists() for concat_file in concat_files)
    assert output_a.read_bytes() == b"merged"
    assert output_b.read_bytes() == b"merged"


@pytest.mark.asyncio
async def test_merge_raises_audio_service_error_on_ffmpeg_failure(tmp_path: Path) -> None:
    segment = tmp_path / "a.mp3"
    output = tmp_path / "episode.mp3"
    segment.write_bytes(b"a")

    with patch(
        "app.services.audio_service.subprocess.run",
        return_value=CompletedFFmpeg(returncode=1, stderr="ffmpeg failed"),
    ):
        with pytest.raises(AudioServiceError, match="ffmpeg failed"):
            await AudioService().merge_mp3_segments([segment], output)
