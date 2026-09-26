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

MODEL = "gemini-1.5-flash"

def _get_api_key() -> str:
    load_dotenv()
    return os.getenv("GEMINI_API_KEY", "").strip()

def _get_model():
    key = _get_api_key()
    if key and GENAI_AVAILABLE and genai is not None:
        try:
            genai.configure(api_key=key)
            return genai.GenerativeModel(MODEL)
        except Exception as e:
            print(f"[AI] GenAI configuration error: {e}")
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
    
    model = _get_model()
    if model:
        try:
            prompt = f"""Extract a list of technical and key domain skills from the following resume/profile text.
Return ONLY a JSON array of strings (max 10 skills). Example: ["Python", "React", "Docker"]
Do not include any other commentary.

Resume:
{resume_text}"""
            response = model.generate_content(prompt)
            skills = _extract_json(response.text)
            if isinstance(skills, list):
                return [str(s) for s in skills[:12]]
        except Exception as e:
            print(f"[AI] extract_skills API error (using heuristic): {e}")

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

    model = _get_model()
    if model:
        try:
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
- reason: 1-2 concise sentences explaining why this member is the best fit
- priority: one of "low", "medium", "high", "critical"

Example format:
[
  {{"task_id": "...", "member_id": "...", "reason": "...", "priority": "high"}}
]"""
            response = model.generate_content(prompt)
            assignments = _extract_json(response.text)
            if isinstance(assignments, list) and len(assignments) > 0:
                return assignments
        except Exception as e:
            print(f"[AI] assign_tasks API error (using heuristic fallback): {e}")

    # Heuristic fallback matching algorithm
    results = []
    member_workload = {m["id"]: 0 for m in members}

    for t in tasks:
        t_text = f"{t.get('title', '')} {t.get('description', '')}".lower()
        best_member = members[0]
        best_score = -1
        best_reason = "Assigned for team workload balance"

        for m in members:
            score = 0
            matched_skills = []
            m_skills = m.get("skills", [])
            for s in m_skills:
                if s.lower() in t_text:
                    score += 3
                    matched_skills.append(s)
            
            if m.get("bio") and any(w in t_text for w in m.get("bio", "").lower().split()):
                score += 1
            
            # Penalize overloaded members slightly
            score -= (member_workload[m["id"]] * 0.5)

            if score > best_score:
                best_score = score
                best_member = m
                if matched_skills:
                    best_reason = f"Strong skill match in {', '.join(matched_skills[:2])}"
                else:
                    best_reason = "Balanced project allocation"

        member_workload[best_member["id"]] += 1

        # Priority calculation heuristic
        priority = "medium"
        if any(w in t_text for w in ["critical", "bug", "urgent", "security", "deploy", "prod"]):
            priority = "critical"
        elif any(w in t_text for w in ["api", "database", "backend", "auth", "core"]):
            priority = "high"
        elif any(w in t_text for w in ["docs", "readme", "comment", "minor", "cleanup"]):
            priority = "low"

        results.append({
            "task_id": t["id"],
            "member_id": best_member["id"],
            "reason": best_reason,
            "priority": t.get("priority") if t.get("priority") in ["low", "medium", "high", "critical"] else priority
        })

    return results

def prioritize_tasks(tasks: list) -> list:
    """Prioritizes tasks by importance and complexity."""
    if not tasks:
        return []

    model = _get_model()
    if model:
        try:
            tasks_summary = [f"- ID: {t['id']}, Title: {t['title']}, Desc: {t.get('description', '')}" for t in tasks]
            prompt = f"""You are a technical project manager. Assign priority ('low', 'medium', 'high', 'critical') to these tasks.
TASKS:
{chr(10).join(tasks_summary)}

Return ONLY a JSON array:
[{{"task_id": "...", "priority": "high", "reason": "..."}}]"""
            response = model.generate_content(prompt)
            res = _extract_json(response.text)
            if isinstance(res, list):
                return res
        except Exception as e:
            print(f"[AI] prioritize_tasks error: {e}")

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
        results.append({"task_id": t["id"], "priority": p, "reason": f"Evaluated based on scope and keywords"})
    return results

def chat(members: list, tasks: list, message: str) -> str:
    """Free-form AI assistant chat."""
    model = _get_model()
    if model:
        try:
            members_summary = [f"- {m['name']}: {', '.join(m.get('skills', [])) or 'General'}" for m in members]
            tasks_summary = [f"- {t['title']} [{t.get('status', 'todo')}] -> {t.get('assigned_to_name', 'Unassigned')} ({t.get('priority', 'medium')})" for t in tasks]

            prompt = f"""You are PIJO AI, an intelligent project manager for student and agile teams.

PROJECT STATUS:
Team Members ({len(members)}):
{chr(10).join(members_summary) or 'None'}

Tasks ({len(tasks)}):
{chr(10).join(tasks_summary) or 'None'}

User Question: {message}

Answer clearly, concisely, and actionably."""
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini API returned an error: {str(e)}"

    # Local intelligent assistant fallback
    msg = message.lower()
    total = len(tasks)
    done = len([t for t in tasks if t.get("status") == "done"])
    todo = len([t for t in tasks if t.get("status") == "todo"])
    unassigned = len([t for t in tasks if not t.get("assigned_to")])

    if "summary" in msg or "status" in msg or "progress" in msg:
        return f"Currently, the team has {len(members)} member(s) and {total} total task(s). {done} done, {todo} to-do, and {unassigned} unassigned. (Running in local heuristic mode. Configure GEMINI_API_KEY in .env for generative LLM responses)."
    elif "who" in msg or "member" in msg or "team" in msg:
        names = [m['name'] for m in members]
        return f"Current team members: {', '.join(names) if names else 'None'}. You can upload member resumes to extract specific skills."
    elif "unassigned" in msg or "assign" in msg:
        return f"There are {unassigned} unassigned tasks. Click '🤖 AI Assign All' on the Tasks board to automatically allocate them!"
    else:
        return f"I analyzed your project with {len(members)} members and {total} tasks ({done}/{total} completed). To unlock natural language generative Q&A, set your `GEMINI_API_KEY` in `.env`."

def generate_summary(members: list, tasks: list) -> str:
    """Generate high-level project health summary."""
    model = _get_model()
    total = len(tasks)
    done = len([t for t in tasks if t.get("status") == "done"])
    in_prog = len([t for t in tasks if t.get("status") == "in_progress"])
    todo = len([t for t in tasks if t.get("status") == "todo"])
    unassigned = len([t for t in tasks if not t.get("assigned_to")])

    if model:
        try:
            prompt = f"""Generate a crisp, encouraging 2-sentence project progress summary.
Stats: {len(members)} members, {total} tasks ({done} done, {in_prog} in progress, {todo} todo, {unassigned} unassigned).
Member names: {', '.join(m['name'] for m in members) or 'None'}."""
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[AI] summary error: {e}")

    # Clean deterministic fallback
    if total == 0:
        return f"Project initialized with {len(members)} member(s). Ready to import tasks and allocate them."
    pct = int((done / total) * 100) if total > 0 else 0
    return f"Project is {pct}% complete ({done}/{total} tasks finished, {in_prog} in progress). {unassigned} task(s) currently unassigned across {len(members)} team member(s)."
