import json
from services.create_docx_service import create_docx
from services.create_pdf_service import create_pdf
from fastapi import (APIRouter,Form,Body,HTTPException)
from fastapi.responses import JSONResponse
from services.gemini_service import generate
from prompts.cover_letter_prompt import (get_cover_letter_prompt)
router = APIRouter(tags=["Cover Letter"])

@router.post("/api/generate-letter")
async def generate_cover_letter(
    job_description: str = Form(...),
    skill_set: str = Form(...),
    applicant_details: str = Form("{}")
        ):
    try:
        details = json.loads(applicant_details)
        prompt = get_cover_letter_prompt(job_description, skill_set, details)
        letter = generate(prompt)
        return JSONResponse({
            "letter" : letter
        })

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