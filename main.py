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
MODEL_NAME = 'gemini-3.1-flash-lite' 

# 3. Initialize FastAPI
app = FastAPI(title="AI Career Coach API")

# 4. Mount Static Files & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
def render_template(template_name: str, request: Request, **context):
    """Simulates Flask's render_template for FastAPI."""
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context=context
    )

# --- PAGE ROUTES (HTML Rendering) ---

@app.get("/")
@app.get("/dashboard")
async def serve_dashboard(request: Request):
    # This correctly points to the templates folder and looks for dashboard.html
    return render_template("dashboard.html", request)

@app.get("/resume")
async def serve_resume_analyzer(request: Request):
    """Renders the ATS Analyzer template."""
    return render_template("resume-analyzer.html", request)

@app.get("/cover-letter")
async def serve_cover_letter(request: Request):
    """Renders the Cover Letter generator template."""
    return render_template("cover-letter.html", request)

@app.get("/interview-prep")
async def serve_interview_prep(request: Request):
    """Renders the Interview Prep template."""
    return render_template("interview-prep.html", request)


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
        
# OUR CODE IS WORKING UNTIL HERE. LETTER GENERATION DOES NOT WORK YET

@app.post("/api/generate-letter")
async def generate_cover_letter(job_description: str = Form(...), skill_set: str = Form(...)):
    """Streams a generated cover letter based on the provided job description."""
    try:
        prompt = f"""
        You are an expert career coach. Write a compelling, highly professional cover letter 
        based on the following job description parameters and the provided Skill set. Do not use generic placeholders like [Company Name] 
        if the data is provided in the description. Keep it concise, impactful, and modern.
        
        Job Parameters:
        {job_description}
        Skill Set:
        {skill_set}
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
        Also provide answers to the questions in pointers and highlight the keywords a candidate should put emphasis on.
        Format this cleanly in a professional manner with pointers explaining on how to approach the answer.
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
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)