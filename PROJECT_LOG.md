# PIJO — Project State Log
> **AI agents: Read this file first to understand the current project state before working on anything.**

## Overview
PIJO is an AI-powered team task manager built for a hackathon.
- **Backend**: Python + FastAPI, JSON file storage in `backend/data/`
- **Frontend**: Neobrutalism Pop-Art UI with Space Grotesk / Plus Jakarta Sans, Lucide Icons & Markdown parsing
- **Animations & Effects**: Interactive particle cursor trail, full-screen celebratory confetti, WebAudio tactile feedback, and 3D card tilt
- **AI Engine**: Google Gemini API (`gemini-3.8-flash` / `gemini-flash-latest`) with resilient heuristic matching fallback
- **Server**: FastAPI at `http://localhost:8000`

## Current Status: 🚀 PRODUCTION & DEMO READY (Phase 1, 2 & Creative Polish)
Last Updated: 2026-09-26

---

## 📁 Repository Structure

```
pijo/
├── backend/
│   ├── main.py              # FastAPI app with static & friendly routing (/members, /tasks)
│   ├── storage.py           # Persistent JSON data storage manager
│   ├── models.py            # Pydantic schemas (Member, Task, StatusUpdate, ChatRequest)
│   ├── ai_service.py        # Gemini API & fallback engine (extract_skills, assign_tasks, prioritize, chat, summary)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── members.py       # Member CRUD & resume/pfp upload endpoints
│   │   ├── tasks.py         # Task CRUD, CSV upload, status updates & AI triggers
│   │   └── ai.py            # AI summary & assistant chat endpoints
│   └── data/
│       ├── members.json     # Member records
│       ├── tasks.json       # Task records
│       └── uploads/         # Stored profile photos & markdown resumes
├── frontend/
│   ├── index.html           # Landing/Dashboard: Hero banner, Sprint meter, stats, AI summary, recent tasks
│   ├── members.html         # Member onboarding card, resume upload & skill extraction
│   ├── tasks.html           # 4-lane Neobrutalist Kanban board (To Do, In Progress, Done, Blocked)
│   ├── css/
│   │   └── style.css        # Complete Neobrutalism design system stylesheet
│   └── js/
│       ├── api.js           # Centralized API fetch client
│       ├── utils.js         # Shared UI helpers (toasts, badges, avatars, Marked.js parser)
│       ├── cursor.js        # Minimal interactive particle cursor trail & click burst
│       └── effects.js       # Full-screen confetti cannon, 3D card tilt, WebAudio synthesizer
├── samples/
│   ├── sample_tasks.csv               # 8 sample team tasks for CSV upload
│   ├── sample_resume_frontend.md      # Frontend engineer markdown resume
│   ├── sample_resume_backend.md       # Backend engineer markdown resume
│   └── sample_resume_ai.md            # AI engineer markdown resume
├── tests/
│   └── test_api.py          # Full end-to-end integration test suite
├── PROJECT_LOG.md           # Architecture & task status tracker
├── README.md                # User & judge documentation
├── requirements.txt         # Python dependencies
└── .env.example             # Template for GEMINI_API_KEY
```

---

## 🚀 Built Features & Verification Checklist

- [x] **Member Management**: Create members with name, bio, profile photo, and resume upload (`/api/members/`)
- [x] **AI Skill Extraction**: Automated skill extraction from markdown/text resumes with AI + fallback (`/api/members/{id}/extract-skills`)
- [x] **Task Ingestion**: CSV file upload parser supporting title, description, and priority (`/api/tasks/upload`)
- [x] **AI Auto-Allocation**: Semantic & skill-matching engine that matches tasks to the best-fit member with explanatory reasons (`/api/tasks/assign`)
- [x] **AI Prioritization**: Automated priority ranking (`low`, `medium`, `high`, `critical`) based on task impact (`/api/tasks/prioritize`)
- [x] **Kanban Board**: 4-column agile board with real-time task status transitions and re-assignment
- [x] **AI Project Assistant**: Floating chat widget with full context of current members and tasks (`/api/ai/chat`)
- [x] **AI Project Summary**: High-level executive project health and progress reporting (`/api/ai/summary`)
- [x] **Markdown Parser**: Live markdown parsing in chatbot for lists, bold text, code blocks, blockquotes
- [x] **Neobrutalism Design**: High-contrast thick borders, pop-art color palette, hard drop shadows, tactile bouncy buttons
- [x] **Landing Hero Section**: Bold high-energy typography, animated badge stickers, and dynamic striped Sprint velocity meter
- [x] **Micro-Interactions**: Particle cursor trail, click burst, 3D card perspective tilt, confetti celebrations on task completion, and tactile audio feedback
- [x] **Automated Test Suite**: End-to-end verification passing in `tests/test_api.py`

---

## ⚡ How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Set your Gemini API key in .env
# GEMINI_API_KEY=your_key_here

# 3. Start the FastAPI server on all interfaces
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```
Open `http://localhost:8000` in the browser.
