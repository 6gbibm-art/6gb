# 🚀 AI Career Coach

> An AI-powered Career Assistant built with **FastAPI**, **Jinja2**, **Vanilla JavaScript**, and **Google Gemini 3.1 Flash Lite**.

AI Career Coach helps students and job seekers improve their resumes, generate professional cover letters, and prepare for interviews using Google's Gemini AI.

---

## ✨ Features

### 📄 ATS Resume Analyzer

- Upload resume in PDF format
- Extracts text using PyMuPDF
- Performs AI-powered ATS analysis
- Generates:
  - Resume score
  - Strengths
  - Weaknesses
  - Missing keywords
  - Improvement suggestions
- Download analysis as PDF

---

### ✉️ AI Cover Letter Generator

Generate personalized cover letters by providing:

- Job Description
- Skill Set
- Applicant Details

Features:

- Professional formatting
- Tailored writing
- Download as:
  - PDF
  - DOCX

---

### 🎤 Interview Preparation

Generate interview preparation guides for any role.

Examples:

- Software Engineer
- Data Analyst
- Frontend Developer
- Backend Developer
- AI Engineer

The generated guide includes:

- Important topics
- Common interview questions
- Technical concepts
- HR questions
- Preparation tips

Download as:

- PDF
- DOCX

---

## 🏗️ Tech Stack

### Backend

- FastAPI
- Uvicorn
- Python 3.12

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Jinja2 Templates

### AI

- Google Gemini 3.1 Flash Lite
- Google GenAI SDK

### Document Processing

- PyMuPDF
- PyPDF2
- ReportLab
- python-docx

### Deployment

- Docker
- Docker Compose
- AWS Ready

---

# 📁 Project Structure

```text
.
├── prompts/
│   ├── ats_prompt.py
│   ├── cover_letter_prompt.py
│   └── interview_prep.py
│
├── routers/
│   ├── pages.py
│   ├── resume.py
│   ├── cover_letter.py
│   └── interview.py
│
├── services/
│   ├── gemini_service.py
│   ├── read_pdf_service.py
│   ├── create_pdf_service.py
│   └── create_docx_service.py
│
├── templates/
├── static/
├── utils/
│
├── config.py
├── main.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

---

# 🧠 Architecture

```
                User
                  │
                  ▼
         FastAPI Routes
                  │
                  ▼
             Prompt Builder
                  │
                  ▼
           Gemini AI Service
                  │
                  ▼
       Generated AI Response
                  │
                  ▼
     HTML / PDF / DOCX Response
```

---

# 🔥 API Endpoints

## Resume Analyzer

| Method | Endpoint |
|---------|-----------|
| POST | `/api/analyze-resume` |
| POST | `/api/download-analysis-pdf` |

---

## Cover Letter

| Method | Endpoint |
|---------|-----------|
| POST | `/api/generate-letter` |
| POST | `/api/download-pdf` |
| POST | `/api/download-docx` |

---

## Interview Preparation

| Method | Endpoint |
|---------|-----------|
| POST | `/api/start-interview` |
| POST | `/api/download-interview-pdf` |
| POST | `/api/download-interview-docx` |

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/<username>/<repository>.git

cd <repository>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env`

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run

```bash
python main.py
```

or

```bash
uvicorn main:app --reload
```

Application runs at

```
http://localhost:8080
```

---

# 🐳 Docker

Build

```bash
docker build -t ai-career-coach .
```

Run

```bash
docker run \
--env-file .env \
-p 8080:8080 \
ai-career-coach
```

---

# 🐳 Docker Compose

Build & Run

```bash
docker compose up --build
```

Stop

```bash
docker compose down
```

---

# ☁️ AWS Deployment

This project is containerized and can be deployed to:

- Amazon App Runner
- Amazon ECS
- EC2
- Azure Container Apps
- Google Cloud Run

Deployment workflow:

```
GitHub
      │
      ▼
Docker Image
      │
      ▼
Amazon ECR
      │
      ▼
AWS App Runner
      │
      ▼
Public HTTPS URL
```

---

# 🔐 Environment Variables

| Variable | Description |
|------------|-------------|
| GEMINI_API_KEY | Google Gemini API Key |

---

# 📸 Screenshots

## Dashboard

> Add dashboard screenshot here

---

## Resume Analyzer

> Add screenshot

---

## Cover Letter Generator

> Add screenshot

---

## Interview Preparation

> Add screenshot

---

# 🚀 Future Improvements

- User Authentication
- Resume History
- Saved Projects
- AI Chat Career Coach
- Job Description Matching
- Resume Keyword Highlighting
- Multi-language Support
- User Dashboard
- Resume Templates
- Dark Mode
- Analytics

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit

```bash
git commit -m "Added feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Mudit**

BCA Student • AI & Backend Developer

Built with ❤️ using FastAPI and Google Gemini.