from config import client, MODEL_NAME
from routers.pages import router as pages_router
from routers.resume import (router as resume_router)
from routers.cover_letter import (router as cover_letter_router)
from routers.interview import (router as interview_router)
import uvicorn
from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Career Coach API")
app.include_router(pages_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(resume_router)
app.include_router(cover_letter_router)
app.include_router(interview_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)