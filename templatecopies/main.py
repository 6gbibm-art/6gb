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
                    yield f"data: {chunk.text}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
# OUR CODE IS WORKING UNTIL HERE. LETTER GENERATION DOES NOT WORK YET

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
                    yield f"data: {chunk.text}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/start-interview")
async def start_interview(role_title: str = Form(...)):
    """Streams interview questions and a roadmap based on the target role."""
    try:
        prompt = f"""
You are a Senior Hiring Manager and Technical Interviewer at a top technology company.

The candidate is preparing for the following role:

ROLE: {role_title}

Generate a professional interview preparation guide in VALID MARKDOWN.

## Formatting Rules
- Return ONLY Markdown.
- Do NOT wrap the response inside triple backticks (```).
- Do NOT return HTML.
- Do NOT use tables.
- Do NOT use emojis.
- Do NOT use horizontal separators (---).
- Use proper Markdown headings (#, ##, ###).
- Use bullet points (-) and numbered lists.
- Use **bold** for important terms.
- Use `inline code` for technologies, SQL keywords, commands, functions, libraries, and syntax.

The response MUST follow this exact structure:

# Interview Guide: {role_title}

A short introduction (2-3 sentences) explaining what interviewers evaluate for this role.

## Technical Interview Questions

Generate EXACTLY 3 highly relevant technical questions.

For EACH question include:

### Question X: <Title>

**Question**

The interview question.

**Key Topics**

- Topic 1
- Topic 2
- Topic 3

**How to Approach**

Provide 3-5 bullet points explaining how the candidate should think about solving the problem.

**Sample Answer**

Provide a concise but high-quality answer in bullet points.

**Common Mistakes**

Mention 2-3 mistakes candidates usually make.

---

## Behavioral Interview Questions

Generate EXACTLY 2 behavioral questions.

For EACH question include:

### Question X: <Title>

**Question**

...

**What the interviewer is evaluating**

- ...

**How to structure your answer**

Explain how to answer using the STAR method.

**Example Talking Points**

Provide bullet points instead of a full scripted answer.

---

## 3-Step Preparation Roadmap

Provide exactly three numbered preparation steps.

For each step include:

### Step X

**Goal**

...

**Tasks**

- ...
- ...
- ...

---

## Interview Tips

Provide 5 practical interview tips.

---

## Final Advice

End with one short paragraph encouraging the candidate to focus on communication, problem solving, and structured thinking.

The guide should be:
- Professional
- Detailed
- Easy to read
- Suitable for FAANG-level interviews
- Tailored specifically for the role: {role_title}
"""

        async def generate():
            response = client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=prompt
            )
            for chunk in response:
                if chunk.text:
                    yield f"data: {chunk.text}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)