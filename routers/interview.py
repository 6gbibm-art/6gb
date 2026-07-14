from fastapi import APIRouter, Form, Body, HTTPException
from fastapi.responses import JSONResponse

from prompts.interview_prep import get_interview_prompt
from services.gemini_service import generate
from services.create_pdf_service import create_pdf
from services.create_docx_service import create_docx

router = APIRouter(tags=["Interview"])


@router.post("/api/start-interview")
async def start_interview(role_title: str = Form(...)):
    try:
        prompt = get_interview_prompt(role_title)

        guide = generate(prompt)

        return JSONResponse({
            "guide": guide
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/download-interview-pdf")
async def download_interview_pdf(data: dict = Body(...)):

    guide = data.get("guide", "")

    if not guide.strip():
        raise HTTPException(
            status_code=400,
            detail="Interview guide is empty."
        )

    return create_pdf(
        content=guide,
        title="Interview Preparation Guide",
        filename="Interview_Guide.pdf"
    )


@router.post("/api/download-interview-docx")
async def download_interview_docx(data: dict = Body(...)):

    guide = data.get("guide", "")

    if not guide.strip():
        raise HTTPException(
            status_code=400,
            detail="Interview guide is empty."
        )

    return create_docx(
        content=guide,
        title="Interview Preparation Guide",
        filename="Interview_Guide.docx"
    )