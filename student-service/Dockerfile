# syntax=docker/dockerfile:1.7
FROM python:3.12-alpine

# Create standard user with UID 1000
RUN addgroup -g 1000 app && adduser -u 1000 -G app -D app

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

CMD ["python", "app.py"]