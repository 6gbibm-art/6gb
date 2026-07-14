from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from prompts.ats_prompt import get_ats_prompt
from services.gemini_service import generate
from services.read_pdf_service import extract_text_from_pdf

router = APIRouter(tags=["Resume"])


@router.post("/api/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    resume_text = await extract_text_from_pdf(file)

    prompt = get_ats_prompt(resume_text)
    report = generate(prompt)

    return JSONResponse({
        "report" : report
    })
    # async def generate():
    #     for chunk in stream_generate(prompt):
    #         yield f"data: {chunk}\n\n"

    #     yield "data: [DONE]\n\n"

    # return StreamingResponse(
    #     generate(),
    #     media_type="text/event-stream"
    # )