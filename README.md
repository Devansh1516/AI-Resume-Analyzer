# AI Resume Analyzer

Modern full-stack resume analysis app built with React, Vite, FastAPI, PyMuPDF, and OpenAI.

## Features

- PDF resume upload with drag-and-drop support
- Resume vs job description ATS score
- Estimated ATS selection probability
- Resume skills, matching job skills, and job-description keyword gap detection
- Targeted improvement suggestions and summary
- Responsive dashboard UI with loading and toast states
- FastAPI backend with typed response validation

## Project Structure

```txt
backend/
  app/
    main.py
    config.py
    routes/resume_routes.py
    services/resume_service.py
    schemas/request_schema.py
    schemas/response_schema.py
    utils/pdf_reader.py
    utils/openai_client.py
    prompts/ats_prompt.py
frontend/
  src/
    components/
    pages/
    services/
    App.jsx
    main.jsx
    index.css
```

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your OpenAI API key to `backend/.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
FRONTEND_ORIGIN=http://localhost:5173
```

Run the API:

```bash
uvicorn app.main:app --reload
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and calls the backend at `http://localhost:8000`.

## API

`POST /api/resume/analyze`

Multipart form data:

- `file`: PDF resume
- `job_description`: Complete pasted job description

Response:

```json
{
  "ats_score": 72,
  "selection_probability": 68,
  "resume_skills": ["React", "JavaScript", "Git"],
  "matched_skills": ["React"],
  "missing_keywords": ["TypeScript", "Redux", "Docker", "AWS"],
  "suggestions": ["Add TypeScript projects", "Include Docker experience", "Mention AWS usage"],
  "summary": "The resume matches most frontend requirements but lacks several technologies required for the role."
}
```

If `OPENAI_API_KEY` is not set, the backend returns a local keyword-based fallback so the app can still be tested end to end.
