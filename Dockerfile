FROM apache/airflow:3.2.1-python3.12

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir .
