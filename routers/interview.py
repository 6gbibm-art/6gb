from fastapi import APIRouter, Form, Body, HTTPException,  Request
from fastapi.responses import StreamingResponse

from prompts.interview_prep import get_interview_prompt
from services.gemini_service import generate_stream
from services.create_pdf_service import create_pdf
from services.create_docx_service import create_docx
from middleware.rate_limiter import limiter, API_RATE_LIMIT

router = APIRouter(tags=["Interview"])


@router.post("/api/start-interview")
@limiter.limit(API_RATE_LIMIT)
async def start_interview(request: Request, role_title: str = Form(...)):
    try:
        prompt = get_interview_prompt(role_title)

        def stream():

            for chunk in generate_stream(prompt):

                yield chunk.encode("utf-8")

        return StreamingResponse(
            stream(),
            media_type="text/plain"
        )

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