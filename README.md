# CareerOS AI

CareerOS AI is an AI career command center for students, recent graduates, and early-career professionals. It helps users manage their profile, analyze resumes, score job fit, tailor application materials, prepare for interviews, identify skill gaps, and track applications.

## Live Demo

Deploy-ready for Streamlit Community Cloud.

- One-click deploy: [Deploy CareerOS AI to Streamlit](https://share.streamlit.io/deploy?repository=https://github.com/Khatiwada5/CareerOS_AI&branch=main&mainModule=app.py)
- App entry point: `app.py`
- Repository: `https://github.com/Khatiwada5/CareerOS_AI`
- Suggested live URL after deployment: `https://careeros-ai.streamlit.app`

To publish the live demo, connect this GitHub repository in [Streamlit Community Cloud](https://streamlit.io/cloud), choose `app.py` as the main file, and add optional secrets for `OPENAI_API_KEY`, `GEMINI_API_KEY`, and `LLM_PROVIDER`.

In Streamlit's **Advanced settings**, choose Python `3.11` or `3.12` for the most reliable dependency install.

## Features

- Home dashboard with profile setup, application counts, average fit score, recent analyses, and follow-up reminders
- Resume Vault for saving an existing PDF, DOCX, or TXT resume
- Resume Analyzer for PDF, DOCX, and TXT uploads
- Job Fit Scorer using the requested 100-point scoring formula
- Resume Tailor that improves bullets without inventing experience
- Cover Letter Generator for short targeted letters
- Interview Prep with likely questions, sample answers, STAR prompts, and recruiter questions
- Skill Gap Planner with missing skills, a 30-day plan, resources, and project ideas
- Application Tracker with add, edit, delete, status, deadline, follow-up date, and notes
- LangGraph workflow with router and specialist agents
- SQLite persistence
- Mock LLM responses when no API key is configured
- Optional OpenAI or Gemini generation when API keys are present
- Lightweight FastAPI backend endpoints

## Tech Stack

- Python
- Streamlit
- FastAPI
- LangGraph
- SQLite
- Pandas
- OpenAI API or Gemini API
- PDF/DOCX resume extraction

## Project Structure

```text
career-os-ai/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── backend/
├── agents/
├── pages/
├── samples/
└── data/
```

## How To Run

```bash
cd career-os-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

The app works without an API key by using deterministic mock LLM responses.

For the full local developer stack, including FastAPI, LangGraph, and pinned package versions:

```bash
pip install -r requirements-full.txt
```

To run the optional FastAPI backend:

```bash
uvicorn backend.api:app --reload
```

## Environment Variables

```text
OPENAI_API_KEY=
GEMINI_API_KEY=
LLM_PROVIDER=openai
DATABASE_PATH=data/careeros.db
```

Set `LLM_PROVIDER=gemini` to use Gemini when `GEMINI_API_KEY` is available.

## Screenshots

Add screenshots here after running the app:

- Home Dashboard
- Resume Analyzer
- Job Fit Scorer
- Application Tracker

## Sample Data

Use these files for quick testing:

- `samples/sample_resume.txt`
- `samples/sample_job_description.txt`

## Fit Score Formula

- Skills match: 40 points
- Experience match: 25 points
- Education match: 15 points
- Project relevance: 10 points
- Keyword match: 10 points

Recommendations:

- 80-100: Strong Apply
- 65-79: Apply with tailoring
- 50-64: Maybe, needs improvement
- Below 50: Low fit

## LangGraph Agent Design

The graph starts with an intent router, then routes work to specialist agents:

- Profile Agent
- Resume Parser / Analyzer Agent
- Job Description Parser Agent
- Fit Scoring Agent
- Resume Tailoring Agent
- Cover Letter Agent
- Interview Coach Agent
- Skill Gap Agent
- Application Tracker Agent
- Final Formatter Agent

## Future Improvements

- Add ChromaDB for profile and resume memory
- Add authenticated multi-user accounts
- Add calendar reminders for follow-ups
- Add richer resume section parsing
- Add role-specific interview modes
- Add export to DOCX/PDF for cover letters and tailored resumes
- Add application analytics charts

## Resume Bullet

Built CareerOS AI, a LangGraph-powered career assistant that analyzes resumes, scores job fit, generates tailored application materials, prepares interview questions, identifies skill gaps, and tracks applications using Python, Streamlit, SQLite, and LLM APIs.
