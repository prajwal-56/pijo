# PIJO — Project State Log
> **AI agents: Read this file first to understand the current project state before working on anything.**

## Overview
PIJO is an AI-powered team task manager built for a hackathon.
- **Backend**: Python + FastAPI with full Multi-Tenant Team Workspace architecture in `backend/data/teams/`
- **Frontend**: Clean Neobrutalism Pop-Art UI (Emoji-Free), Space Grotesk / Plus Jakarta Sans, Lucide SVG Icons & Markdown parsing
- **Multi-Team Workspaces**: Multiple teams/groups can run concurrently on the same server/LAN with isolated members, tasks, and columns. Instant shareable invite URLs (`?team=xyz`)
- **Animations & Effects**: Custom Neobrutal cursor, Antigravity background particle physics, interactive Doodle Pencil tool, full-screen confetti, WebAudio tactile feedback, and 3D card tilt
- **Task Board**: Native Drag-and-Drop Kanban, custom workflow states (e.g. Dropped, In Review), horizontally resizable columns
- **AI Engine**: Google Gemini API (`gemini-3.8-flash` / `gemini-flash-latest`) with resilient heuristic matching fallback
- **Server**: FastAPI at `http://localhost:8000`

## Current Status: 🚀 PRODUCTION & MULTI-TENANT READY
Last Updated: 2026-09-26

---

## 📁 Repository Structure

```
pijo/
├── backend/
│   ├── main.py              # FastAPI app with static & friendly routing (/members, /tasks)
│   ├── storage.py           # Multi-tenant JSON storage (scoped per team in backend/data/teams/{team_id}/)
│   ├── models.py            # Pydantic schemas (Member, Task, StatusUpdate, ChatRequest)
│   ├── ai_service.py        # Gemini API & fallback engine (extract_skills, assign_tasks, prioritize, chat, summary)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── teams.py         # Multi-team workspace CRUD & telemetry endpoints (/api/teams/)
│   │   ├── members.py       # Team-scoped member CRUD & resume/pfp upload endpoints
│   │   ├── tasks.py         # Team-scoped task CRUD, columns CRUD, CSV upload, status updates & AI triggers
│   │   └── ai.py            # Team-scoped AI summary & assistant chat endpoints
│   └── data/
│       ├── teams.json       # Registry of all active team workspaces
│       └── teams/           # Isolated workspace storage directories
│           └── {team_id}/   # Per-team members.json, tasks.json, columns.json
├── frontend/
│   ├── index.html           # Landing/Dashboard: Hero banner, Sprint meter, stats, AI summary, recent tasks
│   ├── members.html         # Member onboarding card, interactive drag & drop avatar preview, skill extraction
│   ├── tasks.html           # Resizable Drag-and-Drop Kanban board with custom column creation
│   ├── css/
│   │   └── style.css        # Complete Neobrutalism design system with workspace dropdown & custom cursor
│   └── js/
│       ├── api.js           # Multi-team API client with X-Team-Id header and ?team= auto-detect
│       ├── teams.js         # Shared team workspace switcher, popover menu, invite links & modal
│       ├── utils.js         # Shared UI helpers (toasts, clean dot badges, avatars, Marked.js parser)
│       ├── cursor.js        # Custom Neobrutal cursor, Antigravity particle physics, and background doodle pencil
│       └── effects.js       # Full-screen confetti cannon, 3D card tilt, WebAudio synthesizer
├── samples/
│   ├── sample_tasks.csv               # 8 sample team tasks for CSV upload & template seeding
│   ├── sample_resume_frontend.md      # Frontend engineer markdown resume
│   ├── sample_resume_backend.md       # Backend engineer markdown resume
│   └── sample_resume_ai.md            # AI engineer markdown resume
├── tests/
│   └── test_api.py          # Full end-to-end integration test suite
├── USER_GUIDE.md            # User-friendly guide with multi-team workflow walkthrough
├── PROJECT_LOG.md           # Architecture & task status tracker
├── README.md                # User & judge documentation
├── requirements.txt         # Python dependencies
└── .env.example             # Template for GEMINI_API_KEY
```

---

## 🚀 Built Features & Verification Checklist

- [x] **Multi-Team Workspaces**: Multiple teams can use the platform concurrently with complete data isolation
- [x] **Team Creation & Seeding**: Create new workspaces with custom names and optional one-click template seeding (3 members, 8 tasks)
- [x] **Workspace Switcher Dropdown**: Fast switching between workspaces from the sidebar on any page
- [x] **1-Click Shareable Invite Links**: Copy `http://<lan-ip>:8000?team={team_id}` to let friends on LAN join the exact team instantly
- [x] **Native Drag-and-Drop Kanban**: Drag task cards seamlessly between columns with live status persistence (`/api/tasks/{id}/status`)
- [x] **Custom Workflow Columns**: Add, persist, and delete custom columns (e.g. "Dropped", "QA", "In Review") via `/api/tasks/columns`
- [x] **Resizable Columns & Chat Modal**: Horizontally resizable Kanban lanes (`resize: horizontal`) and resizable AI chat modal (`resize: both`)
- [x] **Custom Neobrutal Cursor**: Outer tracking ring + inner dot that expands on interactive hover and scales on click
- [x] **Antigravity Particle Physics**: Ambient geometric particles drifting in background that repel and react to cursor movement
- [x] **Doodle Pencil Tool**: Floating toolbar with toggleable pencil mode, color palette, and clear button
- [x] **Interactive Avatar Dropzone**: Drag-and-drop profile photo uploader with real-time thumbnail preview
- [x] **Emoji-Free Professional Aesthetics**: Clean Lucide SVG icons and status indicators
- [x] **AI Auto-Allocation & Prioritization**: Skill matching and priority scoring scoped to the active team
- [x] **Automated Test Suite**: End-to-end verification passing in `tests/test_api.py`
