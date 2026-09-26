# 🚀 PIJO — AI-Powered Team Task Manager

> **Hackathon Edition** — Built for rapid student & team task orchestration, intelligent skill-based automatic task allocation, smart prioritization, and AI assistant Q&A.

---

## ✨ Features

- 👤 **Team Member Profiles**: Create members with name, bio, profile photos, and markdown/text resumes.
- 🧠 **AI Skill Extraction**: Automatically parses resumes/docs and tags extracted technical & domain skills.
- 📁 **CSV Task Ingestion**: Bulk-upload task lists via CSV (`title`, `description`, `priority`).
- 🤖 **AI Automatic Task Allocation**: Semantic & skill-matching engine (powered by Google Gemini with resilient fallback) that analyzes every member's skills vs. task requirements and assigns each task with clear rationale and workload balancing.
- 📊 **Smart Prioritization**: Dynamically categorizes task urgency (`low`, `medium`, `high`, `critical`).
- 📋 **Interactive Kanban Board**: 4-column agile board (`To Do`, `In Progress`, `Done`, `Blocked`) with instant drag-or-select status switching and re-assignment.
- 💬 **Interactive AI Assistant**: Embedded chatbot with live context of all members, current tasks, workloads, and blockers.
- 📈 **Executive Project Summary**: One-click AI health overview and progress reporting.

---

## 🏗️ Architecture

- **Backend**: Python + [FastAPI](https://fastapi.tiangolo.com/) (REST API)
- **Frontend**: Responsive Dark-themed Vanilla HTML5, CSS3, & Modern ES6+ JavaScript
- **AI Intelligence**: Google Gemini API (`gemini-1.5-flash`) + Intelligent keyword & workload heuristic fallback
- **Persistence**: Lightweight JSON file storage (`backend/data/`) — zero database setup required

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Configure Gemini API Key
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and set your key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```
*(Note: PIJO will run with built-in heuristic AI matching even without an API key!)*

### 3. Run the Application
```bash
cd backend
python3 -m uvicorn main:app --reload --port 8000
```

Open your browser and navigate to:
👉 **[http://localhost:8000](http://localhost:8000)**

---

## 🧪 Testing with Sample Data

Ready-to-use sample files are available in the [`samples/`](file:///home/prawmathean/playground/Projects/pijo/samples) directory:
- [`sample_resume_frontend.md`](file:///home/prawmathean/playground/Projects/pijo/samples/sample_resume_frontend.md) — Frontend & UI/UX engineer profile
- [`sample_resume_backend.md`](file:///home/prawmathean/playground/Projects/pijo/samples/sample_resume_backend.md) — Backend & DevOps engineer profile
- [`sample_resume_ai.md`](file:///home/prawmathean/playground/Projects/pijo/samples/sample_resume_ai.md) — AI/ML specialist profile
- [`sample_tasks.csv`](file:///home/prawmathean/playground/Projects/pijo/samples/sample_tasks.csv) — 8 ready-to-import team tasks

### Run the automated test suite:
```bash
python3 tests/test_api.py
```
