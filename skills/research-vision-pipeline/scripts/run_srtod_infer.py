#!/usr/bin/env python3
"""
Placeholder bridge for local SR-TOD inference on experiment videos.

Implement this script by connecting it to the local SR-TOD model codebase.
It should:
1. Accept an input path and output directory
2. Discover videos under the expected metadata directory structure
3. Extract frames
4. Run local counting / detection on frames
4. Write structured detections.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SUPPORTED_VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv"}


def discover_videos(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_VIDEO_EXTS
    ]


def parse_metadata(root: Path, video_path: Path) -> dict[str, str]:
    relative_parts = video_path.relative_to(root).parts
    if len(relative_parts) < 5:
        return {
            "drug_name": "unknown",
            "timestamp": "unknown",
            "species": "unknown",
            "concentration": "unknown",
        }
    return {
        "drug_name": relative_parts[0],
        "timestamp": relative_parts[1],
        "species": relative_parts[2],
        "concentration": relative_parts[3],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--frame-stride", type=int, default=1)
    args = parser.parse_args()

    input_path = Path(args.input_path).resolve()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    videos = discover_videos(input_path)
    payload = {
        "input_path": str(input_path),
        "videos": [
            {
                **parse_metadata(input_path, video_path),
                "file": str(video_path),
                "status": "pending",
                "frames": [],
            }
            for video_path in videos
        ],
        "failures": [],
        "note": "Placeholder script. Connect this to the local SR-TOD backend and replace pending entries with real per-frame counts.",
    }

    (output_dir / "detections.json").write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
