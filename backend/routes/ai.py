from typing import Optional
from fastapi import APIRouter, Header
from models import ChatRequest
from storage import read_members, read_tasks
from ai_service import chat, generate_summary

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/chat")
def ai_chat(body: ChatRequest, x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    members = read_members(x_team_id)
    tasks = read_tasks(x_team_id)
    answer = chat(members, tasks, body.message)
    return {"response": answer}


@router.get("/summary")
def ai_summary(x_team_id: Optional[str] = Header(None, alias="X-Team-Id")):
    members = read_members(x_team_id)
    tasks = read_tasks(x_team_id)
    summary = generate_summary(members, tasks)
    return {"summary": summary}
