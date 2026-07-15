# AI Career Coach

AI Career Coach is a web application that uses Google's Gemini models to assist with different stages of the job application process. The application currently focuses on three core tasks:

- Resume analysis with ATS-style feedback
- AI-generated cover letters
- Interview preparation

I built this project to learn how to integrate large language models into a production-style web application while keeping the stack simple. Instead of using a frontend framework, I chose **FastAPI**, **Jinja2**, and **Vanilla JavaScript** so I could better understand server-side rendering, routing, and backend architecture.

The application is fully Dockerized and can be deployed to cloud platforms such as AWS App Runner.

---

## Features

### Resume Analyzer

Upload a PDF resume and receive detailed AI-generated feedback.

The analysis includes:

- Overall ATS evaluation
- Resume strengths
- Areas that need improvement
- Missing keywords
- Suggestions to improve recruiter visibility

The generated report can also be downloaded as a PDF.

---

### Cover Letter Generator

Generate a professional cover letter by providing:

- Job description
- Applicant information
- Skills and experience

The generated cover letter can be downloaded as either a PDF or a Word document.

---

### Interview Preparation

Generate interview preparation material for any role.

Examples include:

- Software Engineer
- Frontend Developer
- Backend Developer
- Data Analyst
- AI/ML Engineer

Each generated guide contains technical topics, commonly asked interview questions, HR questions, and preparation tips.

The guide can also be exported as PDF or DOCX.

---

## Tech Stack

### Backend

- FastAPI
- Uvicorn

### Frontend

- HTML
- CSS
- Vanilla JavaScript
- Jinja2 Templates

### AI

- Google Gemini
- Google GenAI SDK

### Document Processing

- PyMuPDF
- PyPDF2
- ReportLab
- python-docx

### Deployment

- Docker
- Docker Compose

---

## Project Structure

```
.
├── prompts/
├── routers/
├── services/
├── static/
├── templates/
├── utils/
│
├── config.py
├── main.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

### Folder Overview

| Folder | Purpose |
|---------|----------|
| routers | API endpoints and page routing |
| prompts | Prompt templates sent to Gemini |
| services | Business logic, PDF processing and AI integration |
| templates | Jinja HTML templates |
| static | CSS and JavaScript files |
| utils | Shared helper functions |

---

## How It Works

```
User
   │
   ▼
FastAPI Router
   │
   ▼
Prompt Builder
   │
   ▼
Gemini Service
   │
   ▼
AI Response
   │
   ▼
Rendered HTML / PDF / DOCX
```

---

## Running Locally

Clone the repository

```bash
git clone https://github.com/<your-username>/<repository>.git

cd <repository>
```

Install the dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GEMINI_API_KEY=your_api_key
```

Run the application

```bash
python main.py
```

or

```bash
uvicorn main:app --reload
```

Open

```
http://localhost:8080
```

---

## Running with Docker

Build the image

```bash
docker build -t ai-career-coach .
```

Run the container

```bash
docker run --env-file .env -p 8080:8080 ai-career-coach
```

Or use Docker Compose

```bash
docker compose up --build
```

---

## Environment Variables

Create a `.env` file in the project root.

| Variable | Description |
|----------|-------------|
| GEMINI_API_KEY | Google Gemini API key |

---

## Future Improvements

Some features I'd like to add in the future:

- User authentication
- Resume history
- Saved cover letters
- Job description matching
- Resume keyword highlighting
- Resume scoring dashboard
- AI career chat assistant
- Multi-language support
- User profiles
- Analytics

---

## Lessons Learned

Building this project helped me gain practical experience with:

- FastAPI routing and project organization
- Prompt engineering for LLM applications
- PDF processing in Python
- Dynamic document generation
- Docker and containerization
- Structuring a production-style backend
- Deploying containerized applications

---

## License

This project is licensed under the MIT License.