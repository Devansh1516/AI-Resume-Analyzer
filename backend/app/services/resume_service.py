from app.schemas.response_schema import ResumeAnalysisResponse
from app.utils.openai_client import analyze_resume_with_openai
from app.utils.pdf_reader import extract_text_from_pdf


async def analyze_resume(file_bytes: bytes, job_description: str) -> ResumeAnalysisResponse:
    """Extract resume text and ask OpenAI to compare it with the job description."""

    resume_text = extract_text_from_pdf(file_bytes)
    if len(resume_text.strip()) < 80:
        raise ValueError("Could not extract enough text from this PDF. Try a text-based resume PDF.")

    return await analyze_resume_with_openai(resume_text, job_description)
