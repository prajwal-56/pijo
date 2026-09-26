from fastapi import APIRouter, HTTPException, Body
from typing import Optional
from storage import read_teams, get_team, create_team, delete_team, read_members, read_tasks

router = APIRouter(prefix="/api/teams", tags=["teams"])


@router.get("/")
def list_teams():
    teams = read_teams()
    result = []
    for t in teams:
        members = read_members(t["id"])
        tasks = read_tasks(t["id"])
        done_tasks = len([task for task in tasks if task.get("status") == "done"])
        result.append({
            **t,
            "member_count": len(members),
            "task_count": len(tasks),
            "done_task_count": done_tasks,
        })
    return result


@router.get("/{team_id}")
def get_team_info(team_id: str):
    team = get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    members = read_members(team_id)
    tasks = read_tasks(team_id)
    done_tasks = len([task for task in tasks if task.get("status") == "done"])
    return {
        **team,
        "member_count": len(members),
        "task_count": len(tasks),
        "done_task_count": done_tasks,
    }


@router.post("/", status_code=201)
def create_new_team(payload: dict = Body(...)):
    name = payload.get("name", "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Team name is required")
    description = payload.get("description", "").strip()
    seed_template = bool(payload.get("seed_template", False))
    team = create_team(name=name, description=description, seed_template=seed_template)
    return team


@router.delete("/{team_id}")
def remove_team(team_id: str):
    if team_id == "team-default":
        raise HTTPException(status_code=400, detail="Cannot delete default workspace")
    success = delete_team(team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team not found or cannot be deleted")
    return {"ok": True, "message": "Team deleted"}
