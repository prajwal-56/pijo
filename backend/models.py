from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    blocked = "blocked"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class Member(BaseModel):
    id: str
    name: str
    bio: str = ""
    pfp: Optional[str] = None           # relative URL path
    resume_path: Optional[str] = None   # relative URL path
    resume_text: str = ""               # raw text for AI
    skills: List[str] = Field(default_factory=list)  # AI-extracted
    created_at: str

class Task(BaseModel):
    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    assigned_to: Optional[str] = None   # member id
    assigned_to_name: Optional[str] = None
    assigned_reason: Optional[str] = None
    created_at: str

class StatusUpdate(BaseModel):
    status: TaskStatus

class ChatRequest(BaseModel):
    message: str
