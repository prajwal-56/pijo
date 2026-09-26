# PIJO — Project State Log
> **AI agents: Read this file first to understand the current project state before working on anything.**

## Overview
PIJO is an AI-powered team task manager built for a hackathon.
- **Backend**: Python + FastAPI, JSON file storage in `backend/data/`
- **Frontend**: Clean Neobrutalism Pop-Art UI (Emoji-Free), Space Grotesk / Plus Jakarta Sans, Lucide SVG Icons & Markdown parsing
- **Animations & Effects**: Custom Neobrutal cursor, Antigravity background particle physics, interactive Doodle Pencil tool, full-screen confetti, WebAudio tactile feedback, and 3D card tilt
- **Task Board**: Native Drag-and-Drop Kanban, custom workflow states (e.g. Dropped, In Review), horizontally resizable columns
- **AI Engine**: Google Gemini API (`gemini-3.8-flash` / `gemini-flash-latest`) with resilient heuristic matching fallback
- **Server**: FastAPI at `http://localhost:8000`

## Current Status: 🚀 PRODUCTION & DEMO READY
Last Updated: 2026-09-26

---

## 📁 Repository Structure

```
pijo/
├── backend/
│   ├── main.py              # FastAPI app with static & friendly routing (/members, /tasks)
│   ├── storage.py           # Persistent JSON data storage manager (members, tasks, columns)
│   ├── models.py            # Pydantic schemas (Member, Task, StatusUpdate, ChatRequest)
│   ├── ai_service.py        # Gemini API & fallback engine (extract_skills, assign_tasks, prioritize, chat, summary)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── members.py       # Member CRUD & resume/pfp upload endpoints
│   │   ├── tasks.py         # Task CRUD, columns CRUD, CSV upload, status updates & AI triggers
│   │   └── ai.py            # AI summary & assistant chat endpoints
│   └── data/
│       ├── members.json     # Member records
│       ├── tasks.json       # Task records
│       ├── columns.json     # Custom workflow columns
│       └── uploads/         # Stored profile photos & markdown resumes
├── frontend/
│   ├── index.html           # Landing/Dashboard: Hero banner, Sprint meter, stats, AI summary, recent tasks
│   ├── members.html         # Member onboarding card, interactive drag & drop avatar preview, skill extraction
│   ├── tasks.html           # Resizable Drag-and-Drop Kanban board with custom column creation
│   ├── css/
│   │   └── style.css        # Complete Neobrutalism design system with custom cursor, selection, and doodle toolbar
│   └── js/
│       ├── api.js           # Centralized API fetch client with column endpoints
│       ├── utils.js         # Shared UI helpers (toasts, clean dot badges, avatars, Marked.js parser)
│       ├── cursor.js        # Custom Neobrutal cursor, Antigravity particle physics, and background doodle pencil
│       └── effects.js       # Full-screen confetti cannon, 3D card tilt, WebAudio synthesizer
├── samples/
│   ├── sample_tasks.csv               # 8 sample team tasks for CSV upload
│   ├── sample_resume_frontend.md      # Frontend engineer markdown resume
│   ├── sample_resume_backend.md       # Backend engineer markdown resume
│   └── sample_resume_ai.md            # AI engineer markdown resume
├── tests/
│   └── test_api.py          # Full end-to-end integration test suite
├── USER_GUIDE.md            # User-friendly guide with workflow walkthrough
├── PROJECT_LOG.md           # Architecture & task status tracker
├── README.md                # User & judge documentation
├── requirements.txt         # Python dependencies
└── .env.example             # Template for GEMINI_API_KEY
```

---

## 🚀 Built Features & Verification Checklist

- [x] **Native Drag-and-Drop Kanban**: Drag task cards seamlessly between columns with live status persistence (`/api/tasks/{id}/status`)
- [x] **Custom Workflow Columns**: Add, persist, and delete custom columns (e.g. "Dropped", "QA", "In Review") via `/api/tasks/columns`
- [x] **Resizable Columns & Chat Modal**: Horizontally resizable Kanban lanes (`resize: horizontal`) and resizable AI chat modal (`resize: both`)
- [x] **Custom Neobrutal Cursor**: Outer tracking ring + inner dot that expands on interactive hover and scales on click
- [x] **Antigravity Particle Physics**: Ambient geometric particles drifting in background that repel and react to cursor movement
- [x] **Doodle Pencil Tool**: Floating toolbar with toggleable pencil mode, color palette (black, yellow, pink, cyan), and clear button
- [x] **Custom Highlight/Selection**: High-contrast yellow pop text selection (`::selection`)
- [x] **Interactive Avatar Dropzone**: Drag-and-drop profile photo uploader with real-time thumbnail preview
- [x] **Emoji-Free Professional Aesthetics**: Replaced all clutter emojis with clean Lucide SVG icons and status dots
- [x] **AI Auto-Allocation & Prioritization**: Skill matching and priority scoring with Gemini 3.8 and keyword heuristic fallback
- [x] **Markdown Parser**: Renders AI chat output in formatted HTML with code highlighting and lists

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
