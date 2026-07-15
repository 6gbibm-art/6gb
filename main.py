from config import client, MODEL_NAME
from routers.pages import router as pages_router
from routers.resume import (router as resume_router)
from routers.cover_letter import (router as cover_letter_router)
from routers.interview import (router as interview_router)
from middleware.rate_limiter import limiter
from routers.about import router as about_router

import uvicorn
from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(title="AI Career Coach API")
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": "Too many requests.",
            "message": "Please wait one minute before trying again."
        },
    )
app.include_router(about_router)
app.add_middleware(SlowAPIMiddleware)
app.include_router(pages_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(resume_router)
app.include_router(cover_letter_router)
app.include_router(interview_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)