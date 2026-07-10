import os
import PyPDF2
import uvicorn
from google import genai
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# 1. Load Environment Variables securely
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Please check your .env file.")

# 2. Initialize the Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Note: Make sure this is a valid model name! (e.g., 'gemini-2.5-flash' or 'gemini-1.5-flash')
MODEL_NAME = 'gemini-2.5-flash' 

# 3. Initialize FastAPI
app = FastAPI(title="AI Career Coach API")

# 4. Mount Static Files & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# --- PAGE ROUTES (HTML Rendering) ---

@app.get("/")
async def serve_dashboard(request: Request):
    # This correctly points to the templates folder and looks for dashboard.html
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/resume")
async def serve_resume_analyzer(request: Request):
    """Renders the ATS Analyzer template."""
    return templates.TemplateResponse("resume-analyzer.html", {"request": request})

@app.get("/cover-letter")
async def serve_cover_letter(request: Request):
    """Renders the Cover Letter generator template."""
    return templates.TemplateResponse("cover-letter.html", {"request": request})

@app.get("/interview")
async def serve_interview_prep(request: Request):
    """Renders the Interview Prep template."""
    return templates.TemplateResponse("interview-prep.html", {"request": request})


# --- API ROUTES (AI Processing) ---

@app.post("/api/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    """Accepts a PDF, extracts text, and streams Gemini's ATS analysis."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    try:
        pdf_reader = PyPDF2.PdfReader(file.file)
        resume_text = "".join([page.extract_text() or "" for page in pdf_reader.pages])

        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF.")

        prompt = f"""
        You are an expert ATS (Applicant Tracking System) software and a senior tech recruiter.
        Review the following resume text and provide a strict ATS score out of 100.
        Identify 3 missing keywords, 2 formatting/structural errors, and provide 3 actionable bullet-point improvements.
        Keep your response professional, formatting it clearly for a terminal-style UI.

        Resume Text:
        {resume_text}
        """

        async def generate():
            response = client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=prompt
            )
            for chunk in response:
                if chunk.text:
                    # Replace newlines with HTML breaks for the frontend UI
                    text_chunk = chunk.text.replace("\n", "<br>") 
                    yield f"data: {text_chunk}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-letter")
async def generate_cover_letter(job_description: str = Form(...)):
    """Streams a generated cover letter based on the provided job description."""
    try:
        prompt = f"""
        You are an expert career coach. Write a compelling, highly professional cover letter 
        based on the following job description parameters. Do not use generic placeholders like [Company Name] 
        if the data is provided in the description. Keep it concise, impactful, and modern.
        
        Job Parameters:
        {job_description}
        """

        async def generate():
            response = client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=prompt
            )
            for chunk in response:
                if chunk.text:
                    text_chunk = chunk.text.replace("\n", "<br>")
                    yield f"data: {text_chunk}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/start-interview")
async def start_interview(role_title: str = Form(...)):
    """Streams interview questions and a roadmap based on the target role."""
    try:
        prompt = f"""
        You are a hiring manager interviewing a candidate for the role of: {role_title}.
        Generate 3 highly technical interview questions specific to this role, 
        followed by 2 behavioral questions, and a brief 3-step roadmap on how to prepare.
        Format this cleanly for a terminal UI.
        """

        async def generate():
            response = client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=prompt
            )
            for chunk in response:
                if chunk.text:
                    text_chunk = chunk.text.replace("\n", "<br>")
                    yield f"data: {text_chunk}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)