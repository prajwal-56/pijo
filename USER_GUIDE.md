# PIJO - The Autonomous Team Orchestrator
> **Stop guessing who does what. Allocate by skills.**

Welcome to **PIJO**, your AI-powered task management command center! This guide walks you through how to use the platform to manage hackathon projects, sprint backlogs, and team assignments using Google Gemini AI.

---

## 1. The Dashboard (Mission Control)
When you open PIJO, you'll land on the **Dashboard**. This is your high-level executive overview.
- **Sprint Velocity Meter**: Dynamic striped progress bar that tracks sprint completion in real-time.
- **Executive AI Project Health**: AI-generated readout of how the sprint is progressing.
- **Live Telemetry**: Real-time counts for tasks Completed, In Pipeline, and Awaiting Allocation.
- **Quick Actions**: One-click buttons to run AI assignments or jump straight to the task board.

---

## 2. Onboarding Your Team (Members Page)
PIJO matches tasks to people based on their actual verified skills.

1. Navigate to the **Members** page using the sidebar.
2. Enter the teammate's name and role/bio.
3. **Interactive Photo Dropzone**: Click or drag-and-drop a profile photo to instantly preview their avatar.
4. **Resume Upload**: Upload a `.md`, `.txt`, or `.pdf` file of their resume or skills sheet.
5. Click **Create Member**.
6. **Extract Skills**: Click the **"Extract Skills"** button on their member card. PIJO will parse their resume and generate verified technical skill tags (e.g. `React`, `Python`, `FastAPI`).

---

## 3. The Task Board (Kanban & Custom Workflow States)
Navigate to the **Task Board** to view and manage work.

### Drag and Drop
- Grab any task card and **drag and drop** it directly into another lane (`To Do`, `In Progress`, `Done`, `Blocked`, or any custom state).
- Moving a task to `Done` triggers a celebratory confetti burst.

### Adding Custom Columns / States
- Click the **"Add Column"** button in the top toolbar.
- Enter any custom classification name (e.g. `Dropped`, `In Review`, `QA`, `Backlog`) and pick an accent color.
- Your new column will appear immediately on the board, persisted to the database, and you can drag tasks right into it!
- Custom columns can also be deleted at any time with the delete icon.

### Resizable Layout
- Each Kanban lane is horizontally resizable so you can customize column widths to fit your screen.
- The AI chat modal is also freely resizable from the bottom-right corner.

---

## 4. AI Engine: Auto-Assignment & Prioritization

### Auto-Assignment
Click **"Auto-Assign"** in the top toolbar or from the Dashboard hero banner. 
PIJO analyzes all unassigned tasks, cross-references each task against the extracted skills of your team members, and assigns it to the most qualified person with an explanatory **Match Reason** speech bubble on each card.

### Auto-Prioritization
Click **"Prioritize"** to have Gemini evaluate task criticality and automatically assign priority badges (`Low`, `Medium`, `High`, `Critical`).

---

## 5. Background Doodle Pencil Tool & Interactive Particles
PIJO features an interactive canvas directly on the webpage:
- **Doodle Pencil**: Click the floating **"Pencil"** button docked at the bottom of the screen to activate drawing mode. Select your color (Black, Yellow, Pink, Cyan) and sketch notes, arrows, or doodles across the screen. Click **"Clear"** to erase your drawings or toggle Pencil off to interact with the board normally.
- **Antigravity Particle Physics**: Ambient geometric particles drift across the background and smoothly repel and disperse as you move your cursor near them.
- **Custom Neobrutal Cursor**: A precision dot and follower ring that scales and snaps to interactive elements with high tactile feedback.
- **Custom Selection Color**: Selecting text highlights in high-contrast electric pop yellow.

---

## 6. AI Project Manager Assistant
Click the floating **"Ask PIJO AI"** button in the bottom right corner of any page.

You can ask questions like:
- *"Who is the best person on the team to handle database migrations?"*
- *"Are there any critical tasks currently unassigned?"*
- *"Summarize the current progress and team workload."*

PIJO understands your team's live roster and tasks in real-time and responds with cleanly formatted Markdown (lists, code blocks, bold text).
