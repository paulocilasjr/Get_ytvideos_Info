from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from yt_dlp import YoutubeDL

from ytvideos_info.models import Video, VideoExport

DEFAULT_SOURCE = "https://www.youtube.com/results?search_query=ish+tecnologia&sp=EgQIBRAB"
DEFAULT_OUTPUT = Path("ytvideos_Info_Result.json")
YOUTUBE_WATCH_BASE_URL = "https://www.youtube.com/watch"


def collect_videos(source: str = DEFAULT_SOURCE, *, limit: int = 20) -> VideoExport:
    if limit < 1:
        raise ValueError("limit must be greater than zero")

    with YoutubeDL(_yt_dlp_options()) as ydl:
        info = ydl.extract_info(_normalize_source(source, limit), download=False)

    videos = [
        Video(ID=index, Title=title, URL=url)
        for index, (title, url) in enumerate(_iter_video_metadata(info), start=1)
        if index <= limit
    ]
    return VideoExport(Videos=videos)


def export_videos(
    source: str = DEFAULT_SOURCE,
    *,
    output_path: str | Path = DEFAULT_OUTPUT,
    limit: int = 20,
) -> VideoExport:
    video_export = collect_videos(source, limit=limit)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(_to_legacy_json(video_export), encoding="utf-8")
    return video_export


def _normalize_source(source: str, limit: int) -> str:
    parsed_url = urlparse(source)
    if parsed_url.scheme not in {"http", "https"}:
        return f"ytsearch{limit}:{source}"

    if parsed_url.netloc.endswith("youtube.com") and parsed_url.path == "/results":
        query = parse_qs(parsed_url.query).get("search_query", [""])[0].strip()
        if query:
            return f"ytsearch{limit}:{query}"

    return source


def _yt_dlp_options() -> dict[str, Any]:
    return {
        "extract_flat": "in_playlist",
        "ignoreerrors": True,
        "noplaylist": True,
        "quiet": True,
        "skip_download": True,
    }


def _iter_video_metadata(info: dict[str, Any] | None) -> Iterable[tuple[str, str]]:
    if not info:
        return

    entries = info.get("entries") or [info]
    for entry in entries:
        if not entry:
            continue

        title = (entry.get("title") or "").strip()
        video_url = _video_url(entry)
        if title and video_url:
            yield title, video_url


def _video_url(entry: dict[str, Any]) -> str | None:
    webpage_url = entry.get("webpage_url") or entry.get("url")
    video_id = entry.get("id")

    if isinstance(webpage_url, str) and webpage_url.startswith(("http://", "https://")):
        return webpage_url

    if isinstance(video_id, str) and video_id:
        return f"{YOUTUBE_WATCH_BASE_URL}?v={video_id}"

    return None


def _to_legacy_json(video_export: VideoExport) -> str:
    return json.dumps(
        video_export.model_dump(by_alias=True, mode="json"),
        ensure_ascii=False,
        indent=4,
    )
