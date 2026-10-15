import datetime
import os
from pathlib import Path

from flask import Flask, jsonify, request

os.umask(0)

app = Flask(__name__)
LOG_DIR = Path("/var/log/app")
LOG_PATH = LOG_DIR / "visitas.log"


def get_student_name() -> str:
    return os.getenv("STUDENT_NAME", "Anon")


def get_neighborhood() -> str:
    return os.getenv("BARRIO") or os.getenv("NEIGHBORHOOD") or "Unknown"


@app.before_request
def log_request() -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    msg = f"Hola, I am {get_student_name()} and I live in {get_neighborhood()}"

    try:
        with LOG_PATH.open("a", encoding="utf-8") as log_file:
            log_file.write(f"{msg}\n")
    except OSError:
        pass


@app.get("/")
def home():
    return f"Hola, I am {get_student_name()} and I live in {get_neighborhood()}"


@app.get("/health")
def health():
    return {"ok": True}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
