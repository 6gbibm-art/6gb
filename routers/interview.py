from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
from services.gemini_service import generate
from prompts.interview_prep import get_interview_prompt
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
