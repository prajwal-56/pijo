import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "uploads").mkdir(exist_ok=True)

MEMBERS_FILE = DATA_DIR / "members.json"
TASKS_FILE = DATA_DIR / "tasks.json"

def _init_file(path: Path, default):
    if not path.exists():
        path.write_text(json.dumps(default, indent=2))

_init_file(MEMBERS_FILE, [])
_init_file(TASKS_FILE, [])

def read_members() -> list:
    return json.loads(MEMBERS_FILE.read_text())

def write_members(data: list):
    MEMBERS_FILE.write_text(json.dumps(data, indent=2))

def read_tasks() -> list:
    return json.loads(TASKS_FILE.read_text())

def write_tasks(data: list):
    TASKS_FILE.write_text(json.dumps(data, indent=2))

def uploads_dir() -> Path:
    return DATA_DIR / "uploads"
