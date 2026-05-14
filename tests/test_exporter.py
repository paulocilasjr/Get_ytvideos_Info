import unittest

from ytvideos_info.exporter import _iter_video_metadata, _normalize_source


class ExporterTests(unittest.TestCase):
    def test_normalize_plain_query_uses_ytdlp_search_prefix(self) -> None:
        self.assertEqual(_normalize_source("ish tecnologia", 20), "ytsearch20:ish tecnologia")

    def test_normalize_youtube_results_url_uses_search_query(self) -> None:
        source = "https://www.youtube.com/results?search_query=ish+tecnologia&sp=EgQIBRAB"

        self.assertEqual(_normalize_source(source, 10), "ytsearch10:ish tecnologia")

    def test_iter_video_metadata_prefers_webpage_url(self) -> None:
        info = {
            "entries": [
                {"id": "abc123", "title": "Example", "webpage_url": "https://youtu.be/abc123"},
                {"id": "def456", "title": "Fallback URL"},
                None,
                {"id": "ignored"},
            ]
        }

        self.assertEqual(
            list(_iter_video_metadata(info)),
            [
                ("Example", "https://youtu.be/abc123"),
                ("Fallback URL", "https://www.youtube.com/watch?v=def456"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
