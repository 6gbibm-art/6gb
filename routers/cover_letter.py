import json
from services.create_docx_service import create_docx
from services.create_pdf_service import create_pdf
from fastapi import (APIRouter,Form,Body,HTTPException,  Request)
from fastapi.responses import StreamingResponse
from services.gemini_service import generate, generate_stream
from prompts.cover_letter_prompt import (get_cover_letter_prompt)
from middleware.rate_limiter import limiter, API_RATE_LIMIT

router = APIRouter(tags=["Cover Letter"])

@router.post("/api/generate-letter")
@limiter.limit(API_RATE_LIMIT)
async def generate_cover_letter(
    request: Request,
    job_description: str = Form(...),
    skill_set: str = Form(...),
    applicant_details: str = Form("{}")
        ):
    try:
        details = json.loads(applicant_details)
        prompt = get_cover_letter_prompt(job_description, skill_set, details)
        def stream():

            for chunk in generate_stream(prompt):

                yield chunk.encode("utf-8")

        return StreamingResponse(
            stream(),
            media_type="text/plain"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/download-docx")
async def download_docx(data: dict = Body(...)):
    letter = data.get("letter", "")
    if not letter.strip():
        raise HTTPException(status_code=400, detail="Cover letter is empty.")
    return create_docx(
        content=letter,
        title="Cover Letter",
        filename="Cover_Letter.docx"
    )

@router.post("/api/download-pdf")
async def download_pdf(data: dict = Body(...)):
    letter = data.get("letter", "")
    if not letter.strip():
        raise HTTPException(status_code=400, detail="Cover letter is empty.")
    return create_pdf(
        content=letter,
        title="Cover Letter",
        filename="Cover_Letter.pdf"
    )