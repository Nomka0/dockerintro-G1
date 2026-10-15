# syntax=docker/dockerfile:1.7
FROM python:3.11-slim

# Create standard user with UID 1000
RUN groupadd -g 1000 app && useradd -u 1000 -g app -s /bin/sh app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Create logs directory and ensure shared volume permissions
RUN mkdir -p /var/log/app && chown -R app:app /var/log/app && chmod 777 /var/log/app

USER app

EXPOSE 8080

HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health', timeout=2)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]