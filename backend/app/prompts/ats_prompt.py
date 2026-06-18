def build_ats_prompt(
    resume_text: str,
    job_description: str
) -> str:
    """Create a strict ATS prompt that compares a resume against a job description."""

    return f"""
You are an expert ATS resume evaluator and technical recruiter.

Compare the RESUME against the JOB DESCRIPTION.

Return ONLY valid JSON in exactly this format:

{{
  "ats_score": 72,
  "selection_probability": 68,
  "resume_skills": ["React", "JavaScript", "Git"],
  "matched_skills": ["React"],
  "missing_keywords": ["TypeScript", "Redux", "Docker", "AWS"],
  "suggestions": [
    "Add TypeScript projects",
    "Include Docker experience",
    "Mention AWS usage"
  ],
  "summary": "The resume matches most frontend requirements but lacks several technologies required for the role."
}}

Rules:
- ats_score must be an integer from 0 to 100 and represent the ATS score for this resume against the provided job description.
- selection_probability must be an integer from 0 to 100 estimating the chance this resume passes ATS screening for this specific job.
- selection_probability must be mainly based on the ratio and importance of matched_skills compared with required skills in the job description, then adjusted for missing critical keywords and resume quality.
- resume_skills must contain only concrete skills, tools, frameworks, programming languages, platforms, databases, methodologies, certifications, and technologies actually present in the resume.
- matched_skills must only contain items from resume_skills that also match important requirements in the job description.
- missing_keywords must only contain important skills, tools, frameworks, technologies, certifications, or keywords that appear in the job description but are absent or clearly underrepresented in the resume.
- Missing keywords must come from the actual job description, not from a generic or predefined list.
- Do not put summary/about-section prose, soft traits, normal verbs, first-sentence words, job titles, company descriptions, or generic words such as passionate, responsible, excellent, candidate, team, build, work, ability, and experience in resume_skills, matched_skills, or missing_keywords.
- First extract the job description's required/important technical keywords, then compare those keywords against the resume.
- Suggestions must directly explain how to add or strengthen missing job-description requirements.
- suggestions must be specific, practical, and concise.
- summary must be 1 to 3 sentences.
- Do not include markdown.
- Do not include explanations.
- Do not include extra keys.
- Return JSON only.

JOB DESCRIPTION:
\"\"\"
{job_description[:10000]}
\"\"\"

RESUME:
\"\"\"
{resume_text[:18000]}
\"\"\"
""".strip()
