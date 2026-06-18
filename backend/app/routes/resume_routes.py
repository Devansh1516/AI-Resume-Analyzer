from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.config import settings
from app.schemas.response_schema import ResumeAnalysisResponse
from app.services.resume_service import analyze_resume

router = APIRouter()


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume_route(
    file: UploadFile = File(...),
    job_description: str = Form(...),
) -> ResumeAnalysisResponse:
    """Accept a PDF resume and job description, then return job-specific ATS analysis."""

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    file_bytes = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"PDF must be smaller than {settings.max_upload_mb} MB.",
        )

    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if len(job_description.strip()) < 40:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paste a complete job description before analyzing the resume.",
        )

    try:
        return await analyze_resume(file_bytes, job_description)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
