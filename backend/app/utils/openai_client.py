from __future__ import annotations

import json
import re

import httpx

from app.config import settings
from app.prompts.ats_prompt import build_ats_prompt
from app.schemas.response_schema import ResumeAnalysisResponse


OPENAI_RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"
TECH_SKILLS = [
    ".NET",
    "A/B Testing",
    "Adobe XD",
    "Agile",
    "Airflow",
    "Android",
    "Angular",
    "Ansible",
    "API",
    "Apollo",
    "ASP.NET",
    "AWS",
    "Azure",
    "Babel",
    "BigQuery",
    "Bootstrap",
    "C",
    "C#",
    "C++",
    "CI/CD",
    "CircleCI",
    "CSS",
    "D3.js",
    "Dart",
    "Django",
    "Docker",
    "DynamoDB",
    "Elasticsearch",
    "Express",
    "Figma",
    "Firebase",
    "Flask",
    "Flutter",
    "FastAPI",
    "GCP",
    "Git",
    "GitHub",
    "GitLab",
    "Go",
    "GraphQL",
    "HTML",
    "iOS",
    "Java",
    "JavaScript",
    "Jenkins",
    "Jest",
    "Jira",
    "Kafka",
    "Kubernetes",
    "Laravel",
    "Linux",
    "Machine Learning",
    "MongoDB",
    "MySQL",
    "Next.js",
    "Node.js",
    "NoSQL",
    "NumPy",
    "OpenAI",
    "Pandas",
    "PHP",
    "PostgreSQL",
    "Power BI",
    "Python",
    "PyTorch",
    "React",
    "React Native",
    "Redis",
    "Redux",
    "REST",
    "Ruby",
    "SASS",
    "Scala",
    "Scikit-learn",
    "Scrum",
    "Selenium",
    "SQL",
    "SQLite",
    "Spring Boot",
    "Swift",
    "Tableau",
    "Tailwind",
    "TensorFlow",
    "Terraform",
    "TypeScript",
    "UI/UX",
    "Vue",
    "Webpack",
]

GENERIC_KEYWORDS = {
    "about", "ability", "able", "applicant", "application", "build", "building",
    "candidate", "collaborate", "communication", "company", "customer", "deliver",
    "design", "develop", "developer", "development", "excellent", "experience",
    "experienced", "fast", "good", "high", "highly", "including", "knowledge",
    "looking", "manage", "passionate", "problem", "product", "project", "proven",
    "responsible", "role", "skills", "software", "solution", "strong", "team",
    "using", "work", "working", "written",
}

ATS_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "ats_score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "ATS score for the resume against the job description.",
        },
        "selection_probability": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100,
            "description": "Estimated ATS pass probability based primarily on matched job skills.",
        },
        "resume_skills": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Skills and technologies detected in the resume.",
        },
        "matched_skills": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Detected resume skills that also match important job-description requirements.",
        },
        "missing_keywords": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Important job-description keywords missing from the resume.",
        },
        "suggestions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Specific resume improvement suggestions.",
        },
        "summary": {
            "type": "string",
            "description": "Short recruiter-style summary of the resume.",
        },
    },
    "required": [
        "ats_score",
        "selection_probability",
        "resume_skills",
        "matched_skills",
        "missing_keywords",
        "suggestions",
        "summary",
    ],
    "additionalProperties": False,
}


async def analyze_resume_with_openai(resume_text: str, job_description: str) -> ResumeAnalysisResponse:
    """Send resume text to OpenAI and validate the structured JSON response."""

    if not settings.openai_api_key:
        return _fallback_analysis(resume_text, job_description)

    prompt = build_ats_prompt(resume_text, job_description)
    payload = {
        "model": settings.openai_model,
        "input": [
            {
                "role": "system",
                "content": (
                    "You are an expert ATS resume evaluator and technical recruiter. "
                    "Return accurate, structured JSON only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "resume_ats_analysis",
                "strict": True,
                "schema": ATS_RESPONSE_SCHEMA,
            }
        },
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                OPENAI_RESPONSES_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:500]
        raise RuntimeError(f"OpenAI analysis failed. Check your API key/model. Details: {detail}") from exc
    except httpx.HTTPError as exc:
        raise RuntimeError("OpenAI analysis failed. Check your network connection and try again.") from exc

    candidate_text = _extract_response_text(response.json())
    parsed = _parse_json_object(candidate_text)
    return ResumeAnalysisResponse.model_validate(parsed)


def _extract_response_text(response_data: dict) -> str:
    """Collect text from the Responses API output envelope."""

    if response_data.get("output_text"):
        return response_data["output_text"]

    text_parts: list[str] = []
    for output_item in response_data.get("output", []):
        for content_item in output_item.get("content", []):
            if content_item.get("type") in {"output_text", "text"}:
                text_parts.append(content_item.get("text", ""))

    text = "".join(text_parts).strip()
    if not text:
        raise RuntimeError("OpenAI returned an empty analysis.")

    return text


def _parse_json_object(raw_text: str) -> dict:
    """Parse JSON directly, with a cleanup pass for unexpected fenced responses."""

    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise RuntimeError("OpenAI returned invalid JSON. Please retry the analysis.") from exc


def _fallback_analysis(resume_text: str, job_description: str) -> ResumeAnalysisResponse:
    """Give useful local feedback when OPENAI_API_KEY is not configured."""

    text_lower = resume_text.lower()
    job_keywords = _extract_technical_keywords(job_description)
    resume_skills = _extract_technical_keywords(resume_text)
    matched = [keyword for keyword in job_keywords if keyword.lower() in text_lower]
    missing = [keyword for keyword in job_keywords if keyword.lower() not in text_lower]
    total_keywords = max(len(job_keywords), 1)
    ats_score = round((len(matched) / total_keywords) * 100)
    selection_probability = max(20, min(95, ats_score - min(len(missing) * 2, 18)))

    return ResumeAnalysisResponse(
        ats_score=ats_score,
        selection_probability=selection_probability,
        resume_skills=resume_skills[:16],
        matched_skills=matched[:12],
        missing_keywords=missing[:12],
        suggestions=[
            f"Add direct evidence of {keyword} experience from projects, tools, or achievements."
            for keyword in missing[:4]
        ],
        summary=(
            "OpenAI API key is not configured, so this local analysis estimates the resume match "
            "using keywords extracted from the pasted job description."
        ),
    )


def _extract_job_keywords(job_description: str) -> list[str]:
    """Backward-compatible wrapper for older imports."""

    return _extract_technical_keywords(job_description)


def _extract_technical_keywords(text: str) -> list[str]:
    """Extract concrete technical skills for the no-key local fallback only."""

    found: list[str] = []
    seen: set[str] = set()
    text_lower = text.lower()

    for skill in TECH_SKILLS:
        pattern = r"(?<![A-Za-z0-9+#./-])" + re.escape(skill.lower()) + r"(?![A-Za-z0-9+#./-])"
        if re.search(pattern, text_lower) and skill.lower() not in seen:
            seen.add(skill.lower())
            found.append(skill)

    phrase_candidates = re.findall(
        r"\b(?:[A-Z][A-Za-z0-9+#./-]+|[A-Za-z]+(?:\.js|SQL|API|UI/UX|CI/CD))"
        r"(?:\s+(?:[A-Z][A-Za-z0-9+#./-]+|[A-Za-z]+(?:\.js|SQL|API|UI/UX|CI/CD))){0,2}\b",
        text,
    )

    for candidate in phrase_candidates:
        normalized = candidate.strip(".,:;()[]{}")
        key = normalized.lower()
        if key in seen or key in GENERIC_KEYWORDS:
            continue
        if len(normalized) < 3 or len(normalized.split()) > 3:
            continue
        if not _looks_like_skill(normalized):
            continue
        if _is_combined_existing_skills(normalized, found):
            continue
        seen.add(key)
        found.append(normalized)

    return found[:30]


def _looks_like_skill(value: str) -> bool:
    key = value.lower()
    if key in GENERIC_KEYWORDS:
        return False

    technical_markers = (
        "#", "++", ".js", "sql", "api", "ui/ux", "ci/cd", "cloud", "aws", "azure",
        "react", "docker", "kubernetes", "python", "java", "script", "database",
        "framework", "analytics", "testing",
    )
    if any(marker in key for marker in technical_markers):
        return True

    return value.isupper() and len(value) <= 6


def _is_combined_existing_skills(value: str, found: list[str]) -> bool:
    value_lower = value.lower()
    contained_skills = [
        skill
        for skill in found
        if re.search(r"(?<![A-Za-z0-9+#./-])" + re.escape(skill.lower()) + r"(?![A-Za-z0-9+#./-])", value_lower)
    ]
    return len(contained_skills) >= 2
