from fastapi import APIRouter, File, UploadFile, Body, HTTPException
from fastapi.responses import JSONResponse
from prompts.ats_prompt import get_ats_prompt
from services.gemini_service import generate
from services.read_pdf_service import extract_text_from_pdf
from services.create_pdf_service import create_pdf

router = APIRouter(tags=["Resume"])


@router.post("/api/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
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