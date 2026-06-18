from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ResumeAnalysisResponse(BaseModel):
    ats_score: int = Field(..., ge=0, le=100)
    selection_probability: int = Field(..., ge=0, le=100)
    resume_skills: list[str] = Field(default_factory=list)
    matched_skills: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    summary: str

    @field_validator("resume_skills", "matched_skills", "missing_keywords", "suggestions")
    @classmethod
    def remove_blank_items(cls, values: list[str]) -> list[str]:
        """Clean empty strings from model array output."""

        return [
            item.strip()
            for item in values
            if item and item.strip()
        ]
