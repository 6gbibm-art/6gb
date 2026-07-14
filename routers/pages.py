from fastapi import APIRouter, Request

from utils.template_renderer import render_template

router = APIRouter()


# --- PAGE ROUTES (HTML Rendering) ---
@router.get("/")
@router.get("/dashboard")
async def serve_dashboard(request: Request):
    return render_template("dashboard.html", request, title="Dashboard")

@router.get("/resume")
async def serve_resume_analyzer(request: Request):
    return render_template("resume-analyzer.html", request)

@router.get("/cover-letter")
async def serve_cover_letter(request: Request):
    return render_template("cover-letter.html", request)

@router.get("/interview-prep")
async def serve_interview_prep(request: Request):
    return render_template("interview-prep.html", request)