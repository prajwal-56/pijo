import uuid
import csv
import io
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Body, Header
from fastapi.responses import JSONResponse

from storage import read_tasks, write_tasks, read_members, read_columns, write_columns
from models import TaskPriority, StatusUpdate
from ai_service import assign_tasks, prioritize_tasks

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/columns")
def list_columns(x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    return read_columns(x_team_id)


@router.post("/columns")
def add_column(payload: dict = Body(...), x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    label = payload.get("label", "").strip()
    if not label:
        raise HTTPException(status_code=400, detail="Column label required")
    col_id = payload.get("id") or label.lower().replace(" ", "_")
    color = payload.get("color") or "yellow"
    columns = read_columns(x_team_id)
    if any(c["id"] == col_id for c in columns):
        raise HTTPException(status_code=400, detail="Column ID already exists")
    new_col = {"id": col_id, "label": label, "color": color}
    columns.append(new_col)
    write_columns(columns, x_team_id)
    return new_col


@router.delete("/columns/{col_id}")
def delete_column(col_id: str, x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    columns = read_columns(x_team_id)
    if col_id in ["todo", "done"]:
        raise HTTPException(status_code=400, detail="Cannot delete core column")
    new_cols = [c for c in columns if c["id"] != col_id]
    if len(new_cols) == len(columns):
        raise HTTPException(status_code=404, detail="Column not found")
    write_columns(new_cols, x_team_id)
    return {"ok": True}


@router.get("/")
def list_tasks(x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    return read_tasks(x_team_id)


@router.post("/upload", status_code=201)
async def upload_tasks(file: UploadFile = File(...), x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    """Upload a CSV file. Expected columns: title, description (description optional)."""
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    
    reader = csv.DictReader(io.StringIO(text))
    new_tasks = []
    for row in reader:
        title = row.get("title") or row.get("Title") or row.get("TITLE", "").strip()
        if not title:
            continue
        description = row.get("description") or row.get("Description") or row.get("DESCRIPTION", "").strip()
        priority = row.get("priority") or row.get("Priority") or "medium"
        if priority not in ["low", "medium", "high", "critical"]:
            priority = "medium"
        new_tasks.append({
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "status": "todo",
            "priority": priority,
            "assigned_to": None,
            "assigned_to_name": None,
            "assigned_reason": None,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
    
    tasks = read_tasks(x_team_id)
    tasks.extend(new_tasks)
    write_tasks(tasks, x_team_id)
    return {"added": len(new_tasks), "tasks": new_tasks}


@router.post("/")
def create_task(payload: dict = Body(...), x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    """Create a single task manually."""
    task = {
        "id": str(uuid.uuid4()),
        "title": payload.get("title", "Untitled"),
        "description": payload.get("description", ""),
        "status": "todo",
        "priority": payload.get("priority", "medium"),
        "assigned_to": None,
        "assigned_to_name": None,
        "assigned_reason": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    tasks = read_tasks(x_team_id)
    tasks.append(task)
    write_tasks(tasks, x_team_id)
    return task


@router.patch("/{task_id}/status")
def update_status(task_id: str, body: StatusUpdate, x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    tasks = read_tasks(x_team_id)
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = str(body.status)
            write_tasks(tasks, x_team_id)
            return t
    raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}/assign")
def manual_assign(task_id: str, body: dict = Body(...), x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    """Manually assign a task to a member."""
    members = read_members(x_team_id)
    tasks = read_tasks(x_team_id)
    
    member_id = body.get("member_id")
    member = next((m for m in members if m["id"] == member_id), None)
    if not member and member_id is not None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    for t in tasks:
        if t["id"] == task_id:
            t["assigned_to"] = member_id
            t["assigned_to_name"] = member["name"] if member else None
            t["assigned_reason"] = body.get("reason", "Manually assigned")
            write_tasks(tasks, x_team_id)
            return t
    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/assign")
def ai_assign(x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    """Run AI assignment on all unassigned tasks for this team."""
    members = read_members(x_team_id)
    tasks = read_tasks(x_team_id)
    
    if not members:
        raise HTTPException(status_code=400, detail="No team members found. Add members first.")
    
    unassigned = [t for t in tasks if not t.get("assigned_to")]
    if not unassigned:
        return {"message": "All tasks are already assigned.", "assignments": []}
    
    assignments = assign_tasks(members, unassigned)
    
    if not assignments:
        raise HTTPException(status_code=500, detail="AI assignment failed or returned no results. Check GEMINI_API_KEY.")
    
    # Build member lookup
    member_map = {m["id"]: m["name"] for m in members}
    
    # Apply assignments
    applied = []
    for a in assignments:
        task_id = a.get("task_id")
        member_id = a.get("member_id")
        if not task_id or not member_id:
            continue
        for t in tasks:
            if t["id"] == task_id:
                t["assigned_to"] = member_id
                t["assigned_to_name"] = member_map.get(member_id, "Unknown")
                t["assigned_reason"] = a.get("reason", "")
                t["priority"] = a.get("priority", t.get("priority", "medium"))
                applied.append(t)
                break
    
    write_tasks(tasks, x_team_id)
    return {"message": f"Assigned {len(applied)} tasks.", "assignments": applied}


@router.post("/prioritize")
def ai_prioritize(x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    """Run AI prioritization on all tasks for this team."""
    tasks = read_tasks(x_team_id)
    if not tasks:
        raise HTTPException(status_code=400, detail="No tasks found.")
    
    results = prioritize_tasks(tasks)
    if not results:
        raise HTTPException(status_code=500, detail="AI prioritization failed.")
    
    priority_map = {r["task_id"]: r for r in results}
    for t in tasks:
        if t["id"] in priority_map:
            t["priority"] = priority_map[t["id"]].get("priority", t["priority"])
    
    write_tasks(tasks, x_team_id)
    return {"updated": len(results), "results": results}


@router.delete("/{task_id}")
def delete_task(task_id: str, x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    tasks = read_tasks(x_team_id)
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    write_tasks(new_tasks, x_team_id)
    return {"ok": True}


@router.delete("/")
def clear_tasks(x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    write_tasks([], x_team_id)
    return {"ok": True, "message": "All tasks cleared"}
