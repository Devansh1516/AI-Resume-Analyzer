from __future__ import annotations

from pydantic import BaseModel, Field 


class ResumeAnalysisRequest(BaseModel):
    """Optional schema for text-based testing or future non-file API flows."""

    resume_text: str = Field(..., min_length=80)
