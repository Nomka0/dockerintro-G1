import datetime
import os
from pathlib import Path

from flask import Flask, request

os.umask(0)

app = Flask(__name__)
LOG_PATH = os.getenv("LOG_PATH", "/var/log/app/visitas.log")


def _student_name() -> str:
    return os.getenv("STUDENT_NAME", "Anon")


def _neighborhood() -> str:
    return os.getenv("BARRIO") or os.getenv("NEIGHBORHOOD", "Unknown")


@app.before_request
def log_request() -> None:
    log_file = Path(LOG_PATH)
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    msg = f"Hola, I am {_student_name()} and I live in {_neighborhood()}"
    try:
        with log_file.open("a", encoding="utf-8") as handle:
            handle.write(f"{msg}\n")
    except OSError:
        pass


@app.get("/")
def home() -> tuple[str, int]:
    message = f"Hola, I am {_student_name()} and I live in {_neighborhood()}"
    return message, 200


@app.get("/health")
def health() -> tuple[dict[str, bool], int]:
    return {"ok": True}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
