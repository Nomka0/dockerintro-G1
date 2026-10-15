# syntax=docker/dockerfile:1.7
FROM python:3.11-slim

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p /var/log/app && chown -R app:app /var/log/app

USER app

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD curl -fsS http://localhost:8080/health > /dev/null || exit 1

CMD ["python", "/app/app.py"]
