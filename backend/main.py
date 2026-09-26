import sys
import os
from pathlib import Path

# Ensure backend dir is in path so local imports work
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

from routes.members import router as members_router
from routes.tasks import router as tasks_router
from routes.ai import router as ai_router
from storage import DATA_DIR

app = FastAPI(title="PIJO API", version="1.0.0")

# CORS — allow all origins for hackathon dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
uploads_path = DATA_DIR / "uploads"
uploads_path.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_path)), name="uploads")

# Serve frontend static files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Include routers
app.include_router(members_router)
app.include_router(tasks_router)
app.include_router(ai_router)


@app.get("/health")
def health():
    return {"status": "ok", "app": "PIJO"}


@app.get("/")
def root():
    index = frontend_path / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"message": "PIJO API running. Frontend not found."}


@app.get("/members")
def members_page():
    page = frontend_path / "members.html"
    if page.exists():
        return FileResponse(str(page))
    return FileResponse(str(frontend_path / "index.html"))


@app.get("/tasks")
def tasks_page():
    page = frontend_path / "tasks.html"
    if page.exists():
        return FileResponse(str(page))
    return FileResponse(str(frontend_path / "index.html"))
