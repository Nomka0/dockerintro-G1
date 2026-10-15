import os
import pathlib
import datetime
from fastapi import FastAPI, Request, Response

os.umask(0)

app = FastAPI()

# Environment variables
STUDENT = os.getenv("STUDENT_NAME", "Anon")
BARRIO = os.getenv("BARRIO", "barrio-desconocido")
LOG_PATH = "/var/log/app/visitas.log"

# Ensure log directory exists
try:
    pathlib.Path("/var/log/app").mkdir(parents=True, exist_ok=True)
except OSError:
    pass

def log_visit(request: Request, msg: str):
    """Logs the message to a file."""
    line = f"{msg}\n"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        pass

@app.get("/")
async def root(request: Request):
    """Main entry point returning plain text."""
    msg = f"Hola, I am {STUDENT} and I live in {BARRIO}"
    log_visit(request, msg)
    return Response(content=msg, media_type="text/plain; charset=utf-8")

@app.get("/health")
async def health():
    """Health check endpoint for monitoring."""
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)