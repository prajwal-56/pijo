import json
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
UPLOADS_DIR = DATA_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

TEAMS_FILE = DATA_DIR / "teams.json"
TEAMS_DIR = DATA_DIR / "teams"
TEAMS_DIR.mkdir(exist_ok=True)

DEFAULT_TEAM_ID = "team-default"

DEFAULT_COLUMNS = [
    {"id": "todo", "label": "To Do", "color": "yellow"},
    {"id": "in_progress", "label": "In Progress", "color": "cyan"},
    {"id": "done", "label": "Done", "color": "green"},
    {"id": "blocked", "label": "Blocked", "color": "red"}
]

def _init_file(path: Path, default):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(default, indent=2))

def _init_teams():
    if not TEAMS_FILE.exists():
        default_team = [{
            "id": DEFAULT_TEAM_ID,
            "name": "Alpha Hackers",
            "description": "Primary hackathon command center & sprint workspace",
            "created_at": datetime.now(timezone.utc).isoformat()
        }]
        TEAMS_FILE.write_text(json.dumps(default_team, indent=2))

    default_team_dir = TEAMS_DIR / DEFAULT_TEAM_ID
    default_team_dir.mkdir(exist_ok=True)

    # Legacy migration: if old members.json exists in root data, migrate to team-default
    old_members = DATA_DIR / "members.json"
    old_tasks = DATA_DIR / "tasks.json"
    old_columns = DATA_DIR / "columns.json"

    team_members = default_team_dir / "members.json"
    team_tasks = default_team_dir / "tasks.json"
    team_columns = default_team_dir / "columns.json"

    if old_members.exists() and not team_members.exists():
        shutil.copy(old_members, team_members)
    else:
        _init_file(team_members, [])

    if old_tasks.exists() and not team_tasks.exists():
        shutil.copy(old_tasks, team_tasks)
    else:
        _init_file(team_tasks, [])

    if old_columns.exists() and not team_columns.exists():
        shutil.copy(old_columns, team_columns)
    else:
        _init_file(team_columns, DEFAULT_COLUMNS)

_init_teams()

def _resolve_team_dir(team_id: Optional[str] = None) -> Path:
    if not team_id or team_id.strip() == "":
        team_id = DEFAULT_TEAM_ID
    
    tdir = TEAMS_DIR / team_id
    if not tdir.exists():
        # Fallback to default or create if registered
        teams = read_teams()
        if any(t["id"] == team_id for t in teams):
            tdir.mkdir(parents=True, exist_ok=True)
        else:
            tdir = TEAMS_DIR / DEFAULT_TEAM_ID
            tdir.mkdir(parents=True, exist_ok=True)
            
    _init_file(tdir / "members.json", [])
    _init_file(tdir / "tasks.json", [])
    _init_file(tdir / "columns.json", DEFAULT_COLUMNS)
    return tdir

# =========================================================================
# TEAMS REGISTRY API
# =========================================================================

def read_teams() -> list:
    try:
        return json.loads(TEAMS_FILE.read_text())
    except Exception:
        return [{
            "id": DEFAULT_TEAM_ID,
            "name": "Alpha Hackers",
            "description": "Primary hackathon workspace",
            "created_at": datetime.now(timezone.utc).isoformat()
        }]

def write_teams(data: list):
    TEAMS_FILE.write_text(json.dumps(data, indent=2))

def get_team(team_id: str) -> Optional[dict]:
    teams = read_teams()
    for t in teams:
        if t["id"] == team_id:
            return t
    return None

def create_team(name: str, description: str = "", seed_template: bool = False) -> dict:
    slug = name.lower().strip().replace(" ", "-")
    clean_slug = "".join(c for c in slug if c.isalnum() or c == "-")
    short_code = uuid.uuid4().hex[:6]
    team_id = f"team-{clean_slug}-{short_code}" if clean_slug else f"team-{short_code}"

    team = {
        "id": team_id,
        "name": name.strip(),
        "description": description.strip(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    teams = read_teams()
    teams.append(team)
    write_teams(teams)

    tdir = TEAMS_DIR / team_id
    tdir.mkdir(parents=True, exist_ok=True)
    _init_file(tdir / "columns.json", DEFAULT_COLUMNS)
    _init_file(tdir / "members.json", [])
    _init_file(tdir / "tasks.json", [])

    if seed_template:
        _seed_team_template(tdir)

    return team

def delete_team(team_id: str) -> bool:
    if team_id == DEFAULT_TEAM_ID:
        return False
    teams = read_teams()
    new_teams = [t for t in teams if t["id"] != team_id]
    if len(new_teams) == len(teams):
        return False
    write_teams(new_teams)

    tdir = TEAMS_DIR / team_id
    if tdir.exists():
        shutil.rmtree(tdir)
    return True

def _seed_team_template(tdir: Path):
    samples_dir = Path(__file__).parent.parent / "samples"
    if not samples_dir.exists():
        return

    # Seed members
    members = []
    resume_files = [
        ("Sarah Chen", "Frontend Lead & Design System Specialist", "sample_resume_frontend.md", ["JavaScript", "TypeScript", "React", "CSS", "Tailwind", "Figma", "UI/UX"]),
        ("David Rodriguez", "Senior Backend & DevOps Engineer", "sample_resume_backend.md", ["Python", "FastAPI", "SQL", "PostgreSQL", "Docker", "Kubernetes", "AWS"]),
        ("Maya Patel", "AI Research Engineer & Fullstack Dev", "sample_resume_ai.md", ["Python", "FastAPI", "Machine Learning", "AI", "PyTorch", "TensorFlow"])
    ]

    for name, bio, filename, skills in resume_files:
        fpath = samples_dir / filename
        resume_text = fpath.read_text() if fpath.exists() else ""
        mid = str(uuid.uuid4())
        members.append({
            "id": mid,
            "name": name,
            "bio": bio,
            "pfp": None,
            "resume_path": None,
            "resume_text": resume_text,
            "skills": skills,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
    (tdir / "members.json").write_text(json.dumps(members, indent=2))

    # Seed tasks from sample_tasks.csv
    csv_path = samples_dir / "sample_tasks.csv"
    if csv_path.exists():
        import csv
        import io
        tasks = []
        reader = csv.DictReader(io.StringIO(csv_path.read_text()))
        for row in reader:
            title = row.get("title", "").strip()
            if not title:
                continue
            tasks.append({
                "id": str(uuid.uuid4()),
                "title": title,
                "description": row.get("description", "").strip(),
                "status": "todo",
                "priority": row.get("priority", "medium").lower(),
                "assigned_to": None,
                "assigned_to_name": None,
                "assigned_reason": None,
                "created_at": datetime.now(timezone.utc).isoformat()
            })
        (tdir / "tasks.json").write_text(json.dumps(tasks, indent=2))

# =========================================================================
# TEAM-SCOPED DATA ACCESS
# =========================================================================

def read_members(team_id: Optional[str] = None) -> list:
    tdir = _resolve_team_dir(team_id)
    return json.loads((tdir / "members.json").read_text())

def write_members(data: list, team_id: Optional[str] = None):
    tdir = _resolve_team_dir(team_id)
    (tdir / "members.json").write_text(json.dumps(data, indent=2))

def read_tasks(team_id: Optional[str] = None) -> list:
    tdir = _resolve_team_dir(team_id)
    return json.loads((tdir / "tasks.json").read_text())

def write_tasks(data: list, team_id: Optional[str] = None):
    tdir = _resolve_team_dir(team_id)
    (tdir / "tasks.json").write_text(json.dumps(data, indent=2))

def read_columns(team_id: Optional[str] = None) -> list:
    tdir = _resolve_team_dir(team_id)
    try:
        return json.loads((tdir / "columns.json").read_text())
    except Exception:
        return DEFAULT_COLUMNS

def write_columns(data: list, team_id: Optional[str] = None):
    tdir = _resolve_team_dir(team_id)
    (tdir / "columns.json").write_text(json.dumps(data, indent=2))

def uploads_dir() -> Path:
    return UPLOADS_DIR
