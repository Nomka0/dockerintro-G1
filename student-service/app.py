import os
import pathlib
import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Environment variables
STUDENT = os.getenv("STUDENT_NAME", "Anon")
BARRIO = os.getenv("BARRIO", "barrio-desconocido")
LOG_PATH = "/var/log/app/visitas.log"

# Ensure log directory exists
pathlib.Path("/var/log/app").mkdir(parents=True, exist_ok=True)

def log_visit(path: str, msg: str):
    """Logs the timestamp, client IP, and message to a file."""
    # Use timezone-aware UTC
    ts = datetime.datetime.now(datetime.UTC).isoformat()
    client_ip = request.remote_addr or "unknown"
    line = f"{ts} ip={client_ip} path={path} msg={msg}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)

@app.before_request
def log_incoming_request():
    log_visit(request.path, "incoming request")

@app.get("/")
def root():
    """Main entry point returning plain text."""
    return f"Hola, I am {STUDENT} and I live in {BARRIO}", 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.get("/health")
def health():
    """Health check endpoint for monitoring."""
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)