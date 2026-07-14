import os
import pymupdf
import uvicorn
from google import genai
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from fastapi import Body
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
from Prompts.cover_letter_prompt import get_cover_letter_prompt
from Prompts.ats_prompt import get_ats_prompt
from Prompts.interview_prep import get_interview_prompt
from fastapi.responses import JSONResponse
import json

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
        pdf_bytes = await file.read()

        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

        resume_text = ""

        for page in doc:
            resume_text += page.get_text()

        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from the PDF.")

        prompt = get_ats_prompt(resume_text)

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
        

@app.post("/api/generate-letter")
async def generate_cover_letter(
    job_description: str = Form(...),
    skill_set: str = Form(...),
    applicant_details: str = Form("{}")
        ):
    try:
        details = json.loads(applicant_details)
        prompt = get_cover_letter_prompt(job_description, skill_set, details)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return JSONResponse({
            "letter": response.text
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/download-docx")
async def download_docx(data: dict = Body(...)):
    """
    Generates a downloadable Word document
    from the generated cover letter.
    """

    letter = data.get("letter", "")

    if not letter.strip():
        raise HTTPException(status_code=400, detail="Cover letter is empty.")

    document = Document()

    document.add_heading("Cover Letter", level=1)

    for paragraph in letter.split("\n"):
        document.add_paragraph(paragraph)

    buffer = io.BytesIO()

    document.save(buffer)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition":
            'attachment; filename="Cover_Letter.docx"'
        }
    )
@app.post("/api/download-pdf")
async def download_pdf(data: dict = Body(...)):
    """
    Generates a downloadable PDF
    from the generated cover letter.
    """

    letter = data.get("letter", "")

    if not letter.strip():
        raise HTTPException(status_code=400, detail="Cover letter is empty.")

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Cover Letter</b>", styles["Heading1"]))

    for paragraph in letter.split("\n"):

        if paragraph.strip():

            story.append(
                Paragraph(
                    paragraph.replace("&", "&amp;")
                             .replace("<", "&lt;")
                             .replace(">", "&gt;"),
                    styles["BodyText"]
                )
            )

    doc.build(story)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            'attachment; filename="Cover_Letter.pdf"'
        }
    )


@app.post("/api/start-interview")
async def start_interview(role_title: str = Form(...)):
    """Streams interview questions and a roadmap based on the target role."""
    try:
        prompt = get_interview_prompt(role_title)

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

# @app.on_event("startup")
# async def show_routes():
#     print("\n========== ROUTES ==========")

#     for route in app.routes:
#         methods = ",".join(route.methods or [])
#         print(f"{methods:20} {route.path}")

#     print("============================\n")
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)