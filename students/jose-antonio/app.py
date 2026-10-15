import datetime
import os
from pathlib import Path

from flask import Flask, jsonify, request

os.umask(0)

app = Flask(__name__)
LOG_PATH = "/var/log/app/visitas.log"


def student_name() -> str:
    return os.getenv("STUDENT_NAME", "Antonio Rodriguez Castelblanco")  # Default to "Antonio" if not set


def neighborhood() -> str:
    return os.getenv("BARRIO") or os.getenv("NEIGHBORHOOD", "la Base")


def ensure_log_dir() -> None:
    Path("/var/log/app").mkdir(parents=True, exist_ok=True)


def append_request_log() -> None:
    try:
        ensure_log_dir()
    except OSError:
        pass
    msg = f"Hola, I am {student_name()} and I live in {neighborhood()}"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"{msg}\n")
    except OSError:
        pass


@app.before_request
def log_all_requests() -> None:
    append_request_log()


@app.get("/")
def home() -> str:
    return f"Hola, I am {student_name()} and I live in {neighborhood()}"


@app.get("/health")
def health():
    return {"ok": True}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
 