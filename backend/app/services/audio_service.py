from __future__ import annotations

import asyncio
import subprocess
import tempfile
from collections.abc import Sequence
from pathlib import Path
from uuid import uuid4


FFMPEG_TIMEOUT_SECONDS = 60


class AudioServiceError(Exception):
    pass


class AudioService:
    async def merge_mp3_segments(self, segment_files: Sequence[Path], output_path: Path) -> None:
        if not segment_files:
            raise AudioServiceError("No MP3 segments were provided")

        resolved_segments = [segment.resolve() for segment in segment_files]
        missing_segments = [segment for segment in resolved_segments if not segment.exists()]
        if missing_segments:
            raise AudioServiceError(f"Missing MP3 segment: {missing_segments[0]}")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(prefix="podcast_buddy_ffmpeg_") as temp_dir:
            concat_file = Path(temp_dir) / f"concat_{uuid4().hex}.txt"
            concat_file.write_text(
                "".join(f"file '{self._escape_concat_path(segment)}'\n" for segment in resolved_segments),
                encoding="utf-8",
            )
            await self._run_ffmpeg_concat(concat_file=concat_file, output_path=output_path)

    async def _run_ffmpeg_concat(self, concat_file: Path, output_path: Path) -> None:
        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output_path),
        ]
        loop = asyncio.get_running_loop()

        try:
            result = await loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=FFMPEG_TIMEOUT_SECONDS,
                ),
            )
        except FileNotFoundError as exc:
            raise AudioServiceError("FFmpeg was not found on PATH") from exc
        except subprocess.TimeoutExpired as exc:
            raise AudioServiceError(f"FFmpeg merge timed out after {FFMPEG_TIMEOUT_SECONDS} seconds") from exc
        except OSError as exc:
            raise AudioServiceError(f"Failed to execute FFmpeg: {exc}") from exc

        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "Unknown FFmpeg error").strip()
            raise AudioServiceError(f"FFmpeg merge failed: {detail}")

        if not output_path.exists():
            raise AudioServiceError("FFmpeg completed without creating the merged MP3")

    @staticmethod
    def _escape_concat_path(path: Path) -> str:
        return path.as_posix().replace("'", "'\\''")