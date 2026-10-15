import datetime
import os
from pathlib import Path

from flask import Flask, jsonify, request

os.umask(0)

app = Flask(__name__)
LOG_PATH = os.getenv("LOG_PATH", "/var/log/app/visitas.log")
try:
    Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
except OSError:
    pass


def _student_name() -> str:
    return os.getenv("STUDENT_NAME", "Anon")


def _neighborhood() -> str:
    return os.getenv("BARRIO") or os.getenv("NEIGHBORHOOD") or "Unknown"


@app.before_request
def log_visit() -> None:
    msg = f"Hola, I am {_student_name()} and I live in {_neighborhood()}"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as logfile:
            logfile.write(f"{msg}\n")
    except OSError:
        pass


@app.get("/")
def home() -> str:
    return f"Hola, I am {_student_name()} and I live in {_neighborhood()}"


@app.get("/health")
def health():
    return {"ok": True}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
