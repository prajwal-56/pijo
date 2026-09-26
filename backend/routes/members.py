import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from storage import read_members, write_members, uploads_dir
from ai_service import extract_skills

router = APIRouter(prefix="/api/members", tags=["members"])


@router.get("/")
def list_members():
    return read_members()


@router.get("/{member_id}")
def get_member(member_id: str):
    members = read_members()
    for m in members:
        if m["id"] == member_id:
            return m
    raise HTTPException(status_code=404, detail="Member not found")


@router.post("/", status_code=201)
async def create_member(
    name: str = Form(...),
    bio: str = Form(default=""),
    pfp: Optional[UploadFile] = File(default=None),
    resume: Optional[UploadFile] = File(default=None),
):
    member_id = str(uuid.uuid4())
    uploads = uploads_dir()

    pfp_path = None
    if pfp and pfp.filename:
        ext = Path(pfp.filename).suffix
        fname = f"{member_id}_pfp{ext}"
        fpath = uploads / fname
        fpath.write_bytes(await pfp.read())
        pfp_path = f"/uploads/{fname}"

    resume_text = ""
    resume_path = None
    if resume and resume.filename:
        ext = Path(resume.filename).suffix
        fname = f"{member_id}_resume{ext}"
        fpath = uploads / fname
        content = await resume.read()
        fpath.write_bytes(content)
        resume_path = f"/uploads/{fname}"
        try:
            resume_text = content.decode("utf-8", errors="ignore")
        except Exception:
            resume_text = ""

    # Extract skills with AI
    skills = extract_skills(resume_text) if resume_text else []

    member = {
        "id": member_id,
        "name": name,
        "bio": bio,
        "pfp": pfp_path,
        "resume_path": resume_path,
        "resume_text": resume_text,
        "skills": skills,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    members = read_members()
    members.append(member)
    write_members(members)

    return member


@router.delete("/{member_id}")
def delete_member(member_id: str):
    members = read_members()
    new_members = [m for m in members if m["id"] != member_id]
    if len(new_members) == len(members):
        raise HTTPException(status_code=404, detail="Member not found")
    write_members(new_members)
    return {"ok": True}


@router.post("/{member_id}/extract-skills")
def re_extract_skills(member_id: str):
    """Re-run AI skill extraction for a member."""
    members = read_members()
    for m in members:
        if m["id"] == member_id:
            skills = extract_skills(m.get("resume_text", ""))
            m["skills"] = skills
            write_members(members)
            return {"skills": skills}
    raise HTTPException(status_code=404, detail="Member not found")
