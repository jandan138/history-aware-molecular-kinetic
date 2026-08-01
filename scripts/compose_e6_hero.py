#!/usr/bin/env python3
"""Compose the 45-second E6 Hero master from a rendered E5 source clip.

The source clip is a locked-camera rendering of the frozen E5 bundle.  This script
only retimes, holds, labels, and encodes those pixels; it never interpolates or
alters particle coordinates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compose the E6 45-second Hero")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--fps", type=int, default=24)
    return parser.parse_args()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def _escape_drawtext(value: str) -> str:
    return value.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace("%", "\\\\%")


def _title_filter(title: str, subtitle: str = "") -> str:
    font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    title = _escape_drawtext(title)
    filters = [
        "drawtext="
        f"fontfile={font}:text='{title}':fontcolor=white:fontsize=36:"
        "x=(w-text_w)/2:y=h-92:box=1:boxcolor=0x03050acc:boxborderw=16"
    ]
    if subtitle:
        subtitle = _escape_drawtext(subtitle)
        filters.append(
            "drawtext="
            f"fontfile={font}:text='{subtitle}':fontcolor=0x9ecbd6:fontsize=20:"
            "x=(w-text_w)/2:y=h-43:box=1:boxcolor=0x03050acc:boxborderw=10"
        )
    return ",".join(filters)


def _encode_segment(
    source: Path,
    output: Path,
    *,
    start: float,
    end: float,
    duration: float,
    fps: int,
    title: str,
    subtitle: str,
    reverse: bool = False,
    hold: bool = False,
) -> None:
    target_frames = round(duration * fps)
    if hold:
        filters = (
            f"trim=start={start:.6f}:end={start + 1 / fps:.6f},"
            f"setpts=PTS-STARTPTS,fps={fps},"
            f"tpad=stop_mode=clone:stop_duration={duration:.6f},"
            f"trim=end_frame={target_frames},setpts=N/({fps}*TB)"
        )
    else:
        source_rate = target_frames / max(end - start, 1e-6)
        filters = (
            f"trim=start={start:.6f}:end={end:.6f},setpts=PTS-STARTPTS,"
            f"fps={source_rate:.9f},trim=end_frame={target_frames},"
            f"setpts=N/({fps}*TB)"
        )
        if reverse:
            filters += ",reverse"
    filters += "," + _title_filter(title, subtitle)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(source),
            "-vf",
            filters,
            "-frames:v",
            str(target_frames),
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "17",
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(fps),
            str(output),
        ],
        check=True,
    )


def _compose(args: argparse.Namespace) -> None:
    source = args.source.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if args.fps < 1:
        raise ValueError("fps must be positive")
    source_duration = _duration(source)
    pivot = source_duration * 0.8
    tail_start = max(0.0, source_duration * 0.62)

    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Container duration can extend half a frame beyond the last decodable PTS.
    end_frame = max(0.0, source_duration - 2.0 / args.fps)
    specifications = [
        (0.0, source_duration, 5.0, "A future appears", "Select the middle stroke", False, False),
        (
            tail_start,
            source_duration,
            5.0,
            "Choose what should change",
            "The future is the interface",
            False,
            False,
        ),
        (
            pivot,
            source_duration,
            6.0,
            "Return to the shared visible present",
            "t = 0.80",
            True,
            False,
        ),
        (
            pivot,
            pivot,
            7.0,
            "30 legal physical futures",
            "Browse cached exact EDMD previews",
            False,
            True,
        ),
        (
            pivot,
            pivot,
            6.0,
            "Exchange hidden velocity ownership",
            "2 swaps · 4 of 256 particles",
            False,
            True,
        ),
        (
            pivot,
            source_duration,
            6.0,
            "Same visible present",
            "Two physically recomputed futures",
            False,
            False,
        ),
        (
            end_frame,
            end_frame,
            7.0,
            "Original E  |  Chosen C-like",
            "The selected future happened",
            False,
            True,
        ),
        (
            end_frame,
            end_frame,
            3.0,
            "4 / 256     75 percent     100 percent",
            "Same Present · Chosen Future",
            False,
            True,
        ),
    ]
    with tempfile.TemporaryDirectory(prefix="e6-hero-") as temporary:
        temporary_path = Path(temporary)
        segment_paths = []
        for index, (start, end, duration, title, subtitle, reverse, hold) in enumerate(
            specifications
        ):
            segment_path = temporary_path / f"segment-{index:02d}.mp4"
            _encode_segment(
                source,
                segment_path,
                start=start,
                end=end,
                duration=duration,
                fps=args.fps,
                title=title,
                subtitle=subtitle,
                reverse=reverse,
                hold=hold,
            )
            segment_paths.append(segment_path)
        concat_path = temporary_path / "concat.txt"
        concat_path.write_text(
            "".join(f"file '{path.as_posix()}'\n" for path in segment_paths),
            encoding="utf-8",
        )
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_path),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(output),
            ],
            check=True,
        )

    evidence = {
        "schema_version": "1.0.0",
        "title": "Same Present, Chosen Future",
        "duration_seconds": _duration(output),
        "fps": args.fps,
        "source": {
            "path": source.as_posix(),
            "sha256": _sha256(source),
            "duration_seconds": source_duration,
        },
        "output": {"path": output.as_posix(), "sha256": _sha256(output)},
        "operations": ["trim", "retime", "hold", "caption", "encode"],
        "particle_pixels_warped": False,
        "physics_state_mutated": False,
    }
    manifest_output = args.manifest_output or output.with_suffix(".composition-manifest.json")
    manifest_output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, sort_keys=True))


if __name__ == "__main__":
    _compose(_arguments())
