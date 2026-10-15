import os
import pathlib
from flask import Flask, jsonify, request

os.umask(0)

app = Flask(__name__)
LOG_PATH = os.getenv("LOG_PATH", "/var/log/app/visitas.log")


def _log_request() -> None:
    try:
        pathlib.Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    student_name = os.getenv("STUDENT_NAME", "Anon")
    neighborhood = os.getenv("BARRIO") or os.getenv("NEIGHBORHOOD") or "Unknown"
    msg = f"Hola, I am {student_name} and I live in {neighborhood}"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"{msg}\n")
    except OSError:
        pass


@app.before_request
def log_every_request() -> None:
    _log_request()


@app.get("/")
def home() -> str:
    student_name = os.getenv("STUDENT_NAME", "Anon")
    neighborhood = os.getenv("BARRIO") or os.getenv("NEIGHBORHOOD") or "Unknown"
    return f"Hola, I am {student_name} and I live in {neighborhood}"


@app.get("/health")
def health():
    return {"ok": True}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
