import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from fastapi.testclient import TestClient
from main import app
from storage import write_members, write_tasks

client = TestClient(app)

def test_full_pipeline():
    # Reset storage
    write_members([])
    write_tasks([])

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200, res.text
    print("✓ /health passed")

    # 2. Create Members with sample markdown resumes
    frontend_resume = Path(__file__).parent.parent / "samples" / "sample_resume_frontend.md"
    backend_resume = Path(__file__).parent.parent / "samples" / "sample_resume_backend.md"
    ai_resume = Path(__file__).parent.parent / "samples" / "sample_resume_ai.md"

    # Member 1: Sarah
    with open(frontend_resume, "rb") as f:
        res = client.post(
            "/api/members/",
            data={"name": "Sarah Chen", "bio": "Frontend & UI/UX Specialist"},
            files={"resume": ("sample_resume_frontend.md", f, "text/markdown")}
        )
    assert res.status_code == 201, res.text
    m1 = res.json()
    assert len(m1.get("skills", [])) > 0, "Skills should be extracted"
    print(f"✓ Member 1 created: {m1['name']} with skills: {m1['skills']}")

    # Member 2: David
    with open(backend_resume, "rb") as f:
        res = client.post(
            "/api/members/",
            data={"name": "David Rodriguez", "bio": "Backend & Infrastructure Engineer"},
            files={"resume": ("sample_resume_backend.md", f, "text/markdown")}
        )
    assert res.status_code == 201
    m2 = res.json()
    print(f"✓ Member 2 created: {m2['name']} with skills: {m2['skills']}")

    # Member 3: Maya
    with open(ai_resume, "rb") as f:
        res = client.post(
            "/api/members/",
            data={"name": "Maya Patel", "bio": "AI & ML Engineer"},
            files={"resume": ("sample_resume_ai.md", f, "text/markdown")}
        )
    assert res.status_code == 201
    m3 = res.json()
    print(f"✓ Member 3 created: {m3['name']} with skills: {m3['skills']}")

    # 3. Upload Tasks CSV
    csv_file = Path(__file__).parent.parent / "samples" / "sample_tasks.csv"
    with open(csv_file, "rb") as f:
        res = client.post("/api/tasks/upload", files={"file": ("sample_tasks.csv", f, "text/csv")})
    assert res.status_code == 201, res.text
    tasks_res = res.json()
    assert tasks_res["added"] > 0
    print(f"✓ CSV uploaded: {tasks_res['added']} tasks added")

    # 4. Trigger AI Auto-Assignment
    res = client.post("/api/tasks/assign")
    assert res.status_code == 200, res.text
    assign_res = res.json()
    print(f"✓ AI Assignment complete: {assign_res['message']}")
    for a in assign_res.get("assignments", [])[:3]:
        print(f"   → Task '{a['title']}' assigned to '{a['assigned_to_name']}' (Reason: {a['assigned_reason']})")

    # 5. Trigger AI Prioritization
    res = client.post("/api/tasks/prioritize")
    assert res.status_code == 200, res.text
    print(f"✓ AI Prioritization complete")

    # 6. AI Summary
    res = client.get("/api/ai/summary")
    assert res.status_code == 200, res.text
    print(f"✓ AI Summary: {res.json().get('summary')}")

    # 7. AI Chat
    res = client.post("/api/ai/chat", json={"message": "Who is best suited for UI work and why?"})
    assert res.status_code == 200, res.text
    print(f"✓ AI Chat response: {res.json().get('response')}")

    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_full_pipeline()
