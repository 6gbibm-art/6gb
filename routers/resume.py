from fastapi import APIRouter, File, UploadFile, Body, HTTPException, Request
from fastapi.responses import JSONResponse
from prompts.ats_prompt import get_ats_prompt
from services.gemini_service import generate
from services.read_pdf_service import extract_text_from_pdf
from services.create_pdf_service import create_pdf
from middleware.rate_limiter import limiter, API_RATE_LIMIT

router = APIRouter(tags=["Resume"])


@router.post("/api/analyze-resume")
@limiter.limit(API_RATE_LIMIT)
async def analyze_resume(request: Request, file: UploadFile = File(...)):
    resume_text = await extract_text_from_pdf(file)

    prompt = get_ats_prompt(resume_text)

    report = generate(prompt)

    return JSONResponse({
        "report": report
    })


@router.post("/api/download-analysis-pdf")
async def download_analysis_pdf(data: dict = Body(...)):

    report = data.get("report", "")

    if not report.strip():
        raise HTTPException(
            status_code=400,
            detail="ATS report is empty."
        )

    return create_pdf(
        content=report,
        title="ATS Resume Analysis Report",
        filename="ATS_Report.pdf"
    )