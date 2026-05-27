from __future__ import annotations

import os
from typing import Any

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass


class LLMClient:
    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")

    @property
    def has_real_llm(self) -> bool:
        return bool(self.anthropic_key or self.openai_key or self.gemini_key)

    def generate(self, task: str, context: dict[str, Any]) -> str:
        if self.anthropic_key:
            return self._anthropic_generate(task, context)
        if self.openai_key and self.provider == "openai":
            return self._openai_generate(task, context)
        if self.gemini_key and self.provider == "gemini":
            return self._gemini_generate(task, context)
        return self._mock_generate(task, context)

    def _anthropic_generate(self, task: str, context: dict[str, Any]) -> str:
        from anthropic import Anthropic

        client = Anthropic(api_key=self.anthropic_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1600,
            temperature=0.35,
            system="You are CareerOS AI, a practical career coach. Be specific, concise, and honest. Do not invent experience.",
            messages=[{"role": "user", "content": f"Task: {task}\n\nContext:\n{context}"}],
        )
        return "\n".join(block.text for block in response.content if getattr(block, "type", "") == "text")

    def _openai_generate(self, task: str, context: dict[str, Any]) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self.openai_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are CareerOS AI, a practical career coach. Be specific, concise, and honest. Do not invent experience."},
                {"role": "user", "content": f"Task: {task}\n\nContext:\n{context}"},
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content or ""

    def _gemini_generate(self, task: str, context: dict[str, Any]) -> str:
        import google.generativeai as genai

        genai.configure(api_key=self.gemini_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"You are CareerOS AI, a practical career coach. Do not invent experience.\nTask: {task}\nContext: {context}"
        )
        return response.text or ""

    def _mock_generate(self, task: str, context: dict[str, Any]) -> str:
        role = context.get("role") or context.get("target_role") or "the target role"
        company = context.get("company") or "the company"
        if task == "resume_analysis":
            return (
                "Strengths:\n"
                "- Clear technical and project signals.\n"
                "- Good foundation for early-career applications.\n\n"
                "Weaknesses:\n"
                "- Add more measurable outcomes where truthful.\n"
                "- Make skills easier for ATS systems to scan.\n\n"
                "Suggested bullet improvements:\n"
                "- Built a Python dashboard to analyze application activity and surface follow-up priorities.\n"
                "- Automated data cleanup workflows using Pandas, reducing manual review time where applicable.\n\n"
                "ATS tips:\n"
                "- Mirror important job-description keywords.\n"
                "- Use standard headings: Education, Experience, Projects, Skills."
            )
        if task == "resume_tailor":
            return (
                "- Built data-driven tools using Python and SQL to organize workflows and improve decision-making.\n"
                "- Collaborated with teammates to translate user needs into clear product features and technical tasks.\n"
                "- Developed project documentation, testing notes, and demos for technical and non-technical audiences."
            )
        if task == "cover_letter":
            return (
                f"Dear Hiring Team,\n\n"
                f"I am excited to apply for the {role} position at {company}. My background in projects, analytical problem-solving, "
                "and hands-on technical work gives me a strong foundation to contribute quickly while continuing to learn.\n\n"
                "I am especially interested in this opportunity because it connects practical execution with real business impact. "
                "I would welcome the chance to bring my curiosity, reliability, and project experience to your team.\n\n"
                "Sincerely,\n"
                f"{context.get('name', 'Your Name')}"
            )
        if task == "interview_prep":
            return (
                "Likely questions:\n"
                "1. Tell me about yourself.\n2. Why this role?\n3. Describe a project you are proud of.\n4. How do you handle ambiguity?\n5. What skills are you improving?\n"
                "6. Walk me through a technical/business decision.\n7. Tell me about a time you worked on a team.\n8. How do you prioritize?\n9. Why this company?\n10. What questions do you have?\n\n"
                "Sample STAR answer:\nSituation: In a class or project setting, the team needed a clearer workflow.\nTask: I owned organizing requirements and execution steps.\nAction: I broke the work into milestones, tracked blockers, and communicated progress.\nResult: The team delivered a more complete project and improved collaboration.\n\n"
                "Questions to ask recruiter:\n- What does success look like in the first 90 days?\n- What skills separate strong interns or early-career hires on this team?"
            )
        if task == "skill_gap":
            return (
                "Missing skills to prioritize:\n- SQL\n- Role-specific tools from the job description\n- Clearer portfolio evidence\n\n"
                "30-day plan:\nWeek 1: Review fundamentals and complete short tutorials.\nWeek 2: Build a small role-relevant project.\nWeek 3: Add metrics, documentation, and a README.\nWeek 4: Tailor resume bullets and practice interview stories.\n\n"
                "Free resources:\n- freeCodeCamp\n- Kaggle Learn\n- Google/Coursera audit options\n- Official tool documentation\n\n"
                "Project ideas:\n- Build a dashboard or workflow tool connected to the target role.\n- Analyze a public dataset and write a short business memo."
            )
        return "CareerOS AI generated a practical next step based on your profile and job context."
