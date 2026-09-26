from fastapi import APIRouter
from models import ChatRequest
from storage import read_members, read_tasks
from ai_service import chat, generate_summary

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/chat")
def ai_chat(body: ChatRequest):
    members = read_members()
    tasks = read_tasks()
    answer = chat(members, tasks, body.message)
    return {"response": answer}


@router.get("/summary")
def ai_summary():
    members = read_members()
    tasks = read_tasks()
    summary = generate_summary(members, tasks)
    return {"summary": summary}
