from __future__ import annotations

import pendulum
from airflow.sdk import dag, task

from ytvideos_info.exporter import DEFAULT_SOURCE, export_videos


@dag(
    dag_id="ytvideos_info_export",
    description="Export YouTube search result titles and URLs to JSON.",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule="*/5 * * * *",
    catchup=False,
    tags=["youtube", "metadata"],
)
def ytvideos_info_export() -> None:
    @task(retries=1)
    def export_search_results() -> int:
        video_export = export_videos(
            DEFAULT_SOURCE,
            output_path="/opt/airflow/output/ytvideos_Info_Result.json",
            limit=20,
        )
        return len(video_export.videos)

    export_search_results()


ytvideos_info_export()
