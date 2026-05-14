# ytvideos-info

Modern Python rewrite of the original Scrapy + Airflow YouTube metadata exporter.

The project exports the first videos for a YouTube search query or results URL to the original JSON shape:

```json
{
  "Videos": [
    {
      "ID": 1,
      "Title": "Video title",
      "URL": "https://www.youtube.com/watch?v=..."
    }
  ]
}
```

## What changed

- Replaced brittle `ytInitialData` HTML parsing with `yt-dlp`, which tracks YouTube extractor changes.
- Replaced ad-hoc scripts with an installable Python package and CLI.
- Added Pydantic validation for exported records.
- Updated the Airflow DAG to Airflow 3 public APIs via `airflow.sdk`.
- Simplified local orchestration to a single Airflow container for this small scheduled job.
- Added Ruff configuration and unit tests for the core parsing behavior.

Current dependency baseline checked on May 14, 2026:

- Apache Airflow `3.2.1`
- Python `3.12+`
- Pydantic `2.13+`
- Ruff `0.15+`
- yt-dlp `2026.3.17+`

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ytvideos-info "ish tecnologia" --limit 20 --output ytvideos_Info_Result.json
```

You can also pass the legacy YouTube results URL:

```bash
ytvideos-info "https://www.youtube.com/results?search_query=ish+tecnologia&sp=EgQIBRAB"
```

## Run with Airflow

```bash
docker compose up --build
```

Airflow is available at `http://localhost:8080`. In standalone mode, Airflow prints the
generated admin login credentials in the container logs. The scheduled DAG writes to
`output/ytvideos_Info_Result.json`.

## Validate

```bash
python -m unittest
ruff check .
ruff format --check .
```
