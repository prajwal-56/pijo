import os
import json
import re
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    genai = None
    GENAI_AVAILABLE = False

# Active Gemini models with automatic failover
ACTIVE_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-lite-latest",
    "gemma-4-26b-a4b-it",
    "gemini-3.8-flash",
]

def _get_api_key() -> str:
    load_dotenv()
    return os.getenv("GEMINI_API_KEY", "").strip()

def _generate_content(prompt: str) -> Optional[str]:
    """Execute generate_content with dynamic multi-model failover."""
    key = _get_api_key()
    if not key or not GENAI_AVAILABLE or genai is None:
        return None

    try:
        genai.configure(api_key=key)
    except Exception as e:
        print(f"[AI] GenAI configure error: {e}")
        return None

    for model_name in ACTIVE_MODELS:
        try:
            m = genai.GenerativeModel(model_name)
            res = m.generate_content(prompt)
            if res and res.text:
                return res.text
        except Exception as e:
            # If quota or model error, try next candidate model
            err_msg = str(e).split('\n')[0]
            print(f"[AI] Model {model_name} error ({err_msg[:60]}), trying next candidate...")
            continue
    return None

def _extract_json(text: str):
    """Extract JSON from a model response that may have markdown fences."""
    text = text.strip()
    match = re.search(r'```(?:json)?\s*([\s\S]+?)\s*```', text)
    if match:
        text = match.group(1)
    return json.loads(text)

# Common tech/skill vocabulary for heuristic fallback
COMMON_SKILLS = [
    "Python", "JavaScript", "TypeScript", "React", "Vue", "Angular", "Node.js", "FastAPI",
    "Django", "Flask", "SQL", "PostgreSQL", "MongoDB", "Docker", "Kubernetes", "AWS",
    "GCP", "Azure", "Git", "GitHub", "HTML", "CSS", "Tailwind", "Machine Learning", "AI",
    "PyTorch", "TensorFlow", "Pandas", "NumPy", "Figma", "UI/UX", "GraphQL", "REST API",
    "CI/CD", "Linux", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "Flutter"
]

def extract_skills(resume_text: str) -> List[str]:
    """Extract skill tags from a resume/markdown text with AI or heuristic fallback."""
    if not resume_text or not resume_text.strip():
        return []
    
    prompt = f"""Extract a list of technical and key domain skills from the following resume/profile text.
Return ONLY a JSON array of strings (max 10 skills). Example: ["Python", "React", "Docker"]
Do not include any other commentary.

Resume:
{resume_text}"""

    raw = _generate_content(prompt)
    if raw:
        try:
            skills = _extract_json(raw)
            if isinstance(skills, list):
                return [str(s) for s in skills[:12]]
        except Exception as e:
            print(f"[AI] extract_skills JSON parse error: {e}")

    # Heuristic fallback if no API key or API call failed
    found = []
    text_lower = resume_text.lower()
    for skill in COMMON_SKILLS:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            found.append(skill)
    return found[:10]

def assign_tasks(members: list, tasks: list) -> list:
    """
    Assign tasks to members based on skill match.
    Uses Gemini API if key is present; otherwise applies smart skill-matching heuristic.
    """
    if not members or not tasks:
        return []

    members_summary = []
    for m in members:
        skills_str = ", ".join(m.get("skills", [])) or "General development"
        members_summary.append(
            f"- ID: {m['id']}\n  Name: {m['name']}\n  Skills: {skills_str}\n  Bio: {m.get('bio', '')}\n  Resume: {m.get('resume_text', '')[:400]}"
        )
    
    tasks_summary = []
    for t in tasks:
        tasks_summary.append(
            f"- ID: {t['id']}\n  Title: {t['title']}\n  Description: {t.get('description', '')}"
        )

    prompt = f"""You are an expert project manager AI. Assign each task to the most suitable team member based on their skills and background. Balance the workload when possible.

TEAM MEMBERS:
{chr(10).join(members_summary)}

TASKS TO ASSIGN:
{chr(10).join(tasks_summary)}

Return ONLY a JSON array. Each element must have:
- task_id: the task ID string
- member_id: the best-fit member ID string
- reason: 1-2 sentence explanation of why this member fits best
- priority: one of "low", "medium", "high", "critical" based on importance

Example:
[
  {{"task_id": "abc", "member_id": "xyz", "reason": "Sarah has strong React & UI skills required for this component.", "priority": "high"}}
]

Do not include any extra text."""

    raw = _generate_content(prompt)
    if raw:
        try:
            assignments = _extract_json(raw)
            if isinstance(assignments, list) and len(assignments) > 0:
                return assignments
        except Exception as e:
            print(f"[AI] assign_tasks JSON parse error: {e}")

    # Fallback heuristic assignment algorithm
    print("[AI] Using keyword heuristic for task assignment")
    return _heuristic_assign_tasks(members, tasks)

def _heuristic_assign_tasks(members: list, tasks: list) -> list:
    """
    Deterministic skill-matching heuristic that scores member suitability
    based on resume skills and task keywords, while balancing workload.
    """
    assignments = []
    member_workload = {m["id"]: 0 for m in members}

    for task in tasks:
        task_text = f"{task.get('title', '')} {task.get('description', '')}".lower()
        best_member = None
        best_score = -1
        matching_skills = []

        for m in members:
            score = 0
            member_skills = m.get("skills", [])
            member_matched = []
            
            for skill in member_skills:
                if skill.lower() in task_text:
                    score += 3
                    member_matched.append(skill)
            
            bio_text = f"{m.get('bio', '')} {m.get('resume_text', '')[:300]}".lower()
            for word in task_text.split():
                if len(word) > 4 and word in bio_text:
                    score += 1

            # Workload balancing penalty
            score -= (member_workload[m["id"]] * 1.5)

            if score > best_score:
                best_score = score
                best_member = m
                matching_skills = member_matched

        if not best_member:
            best_member = min(members, key=lambda m: member_workload[m["id"]])

        member_workload[best_member["id"]] += 1

        if matching_skills:
            reason = f"Strong skill match in {', '.join(matching_skills[:3])}"
        elif best_member.get("bio"):
            reason = f"Aligned with role: {best_member['bio'][:50]}"
        else:
            reason = "Balanced project allocation"

        assignments.append({
            "task_id": task["id"],
            "member_id": best_member["id"],
            "reason": reason,
            "priority": task.get("priority", "medium")
        })

    return assignments

def prioritize_tasks(tasks: list) -> list:
    """Assign smart priority to tasks using AI or heuristics."""
    if not tasks:
        return []

    tasks_summary = [f"- ID: {t['id']}, Title: {t['title']}, Description: {t.get('description', '')}" for t in tasks]

    prompt = f"""You are a technical project manager. Prioritize these tasks for a development sprint.
Assign each task: "low", "medium", "high", or "critical".

TASKS:
{chr(10).join(tasks_summary)}

Return ONLY a JSON array:
[
  {{"task_id": "...", "priority": "high", "reason": "1-sentence reason"}}
]"""

    raw = _generate_content(prompt)
    if raw:
        try:
            results = _extract_json(raw)
            if isinstance(results, list):
                return results
        except Exception as e:
            print(f"[AI] prioritize_tasks JSON error: {e}")

    # Heuristic fallback
    results = []
    for t in tasks:
        txt = f"{t.get('title', '')} {t.get('description', '')}".lower()
        if any(w in txt for w in ["auth", "security", "crash", "bug", "blocker", "critical", "database"]):
            p = "critical"
        elif any(w in txt for w in ["api", "core", "pipeline", "backend", "setup", "feature"]):
            p = "high"
        elif any(w in txt for w in ["style", "docs", "readme", "cleanup", "minor"]):
            p = "low"
        else:
            p = "medium"
        results.append({"task_id": t["id"], "priority": p, "reason": "Evaluated based on scope and keywords"})
    return results

def chat(members: list, tasks: list, message: str) -> str:
    """Free-form AI assistant chat with full project context and multi-model failover."""
    members_summary = [f"- {m['name']}: {', '.join(m.get('skills', [])) or 'General'}" for m in members]
    tasks_summary = [f"- {t['title']} [{t.get('status', 'todo')}] -> {t.get('assigned_to_name', 'Unassigned')} ({t.get('priority', 'medium')})" for t in tasks]

    prompt = f"""You are PIJO AI, an intelligent project manager for student and agile teams.

PROJECT STATUS:
Team Members ({len(members)}):
{chr(10).join(members_summary) or 'None'}

Tasks ({len(tasks)}):
{chr(10).join(tasks_summary) or 'None'}

User Question: {message}

Answer clearly, concisely, and actionably in clean Markdown."""

    response_text = _generate_content(prompt)
    if response_text and response_text.strip():
        return response_text.strip()

    # Local intelligent assistant fallback only if all API models fail
    msg = message.lower()
    total = len(tasks)
    done = len([t for t in tasks if t.get("status") == "done"])
    todo = len([t for t in tasks if t.get("status") == "todo"])
    unassigned = len([t for t in tasks if not t.get("assigned_to")])

    if "summary" in msg or "status" in msg or "progress" in msg:
        return f"Currently, the team has {len(members)} member(s) and {total} total task(s). {done} done, {todo} to-do, and {unassigned} unassigned."
    elif "who" in msg or "member" in msg or "team" in msg:
        names = [m['name'] for m in members]
        return f"Current team members: {', '.join(names) if names else 'None'}. You can upload member resumes to extract specific skills."
    elif "unassigned" in msg or "assign" in msg:
        return f"There are {unassigned} unassigned tasks. Click 'Auto-Assign' on the Tasks board to automatically allocate them!"
    else:
        return f"Based on the project state with {len(members)} members and {total} tasks ({done}/{total} completed), everything is on track. How can I help you plan further?"

def generate_summary(members: list, tasks: list) -> str:
    """Generate high-level project health summary."""
    total = len(tasks)
    done = len([t for t in tasks if t.get("status") == "done"])
    in_prog = len([t for t in tasks if t.get("status") == "in_progress"])
    todo = len([t for t in tasks if t.get("status") == "todo"])
    unassigned = len([t for t in tasks if not t.get("assigned_to")])

    prompt = f"""Generate a crisp, encouraging 2-sentence project progress summary.
Stats: {len(members)} members, {total} tasks ({done} done, {in_prog} in progress, {todo} todo, {unassigned} unassigned).
Member names: {', '.join(m['name'] for m in members) or 'None'}."""

    response_text = _generate_content(prompt)
    if response_text and response_text.strip():
        return response_text.strip()

    # Clean deterministic fallback
    if total == 0:
        return f"Project initialized with {len(members)} member(s). Ready to import tasks and allocate them."
    pct = int((done / total) * 100) if total > 0 else 0
    return f"Project is {pct}% complete ({done}/{total} tasks finished, {in_prog} in progress). {unassigned} task(s) currently unassigned across {len(members)} team member(s)."
