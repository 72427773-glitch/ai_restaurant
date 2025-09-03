import os
from datetime import datetime

LOGS_PATH = os.path.join("app", "data", "logs")
os.makedirs(LOGS_PATH, exist_ok=True)
LOG_FILE = os.path.join(LOGS_PATH, "errores.log")

def registrar_error(contexto: str, error: Exception):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(sep=' ', timespec='seconds')}] {contexto}: {repr(error)}\n")
