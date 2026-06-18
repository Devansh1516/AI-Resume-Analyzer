from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.resume_routes import router as resume_router


app = FastAPI(
    title="AI Resume Analyzer API",
    description="FastAPI backend that extracts PDF resume text and analyzes it with OpenAI.",
    version="1.0.0",
)

# CORS allows the Vite frontend to call the API during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(resume_router, prefix="/api/resume", tags=["Resume"])
