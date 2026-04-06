#!/usr/bin/env python3
"""
Placeholder aggregation script.

Reads detections.json and emits a minimal summary.json.
Replace with real aggregation logic once the SR-TOD output contract is finalized.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--detections-json", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    detections = json.loads(Path(args.detections_json).read_text())
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "total_videos": len(detections.get("videos", [])),
        "processed_videos": len(
            [item for item in detections.get("videos", []) if item.get("status") == "ok"]
        ),
        "failed_videos": len(detections.get("failures", [])),
        "counts_by_species": {},
        "counts_by_concentration": {},
        "note": "Placeholder aggregation. Implement per-video and time-series counting here.",
    }

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
