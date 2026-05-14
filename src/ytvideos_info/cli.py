from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ytvideos_info.exporter import DEFAULT_OUTPUT, DEFAULT_SOURCE, export_videos


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export YouTube video metadata to JSON.")
    parser.add_argument(
        "source",
        nargs="?",
        default=DEFAULT_SOURCE,
        help="YouTube URL or search query to export.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON output path.",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=20,
        help="Maximum number of videos to export.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    video_export = export_videos(args.source, output_path=args.output, limit=args.limit)
    print(f"Wrote {len(video_export.videos)} videos to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
