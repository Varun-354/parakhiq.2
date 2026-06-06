# importing LLM MODEL OF GROQ
from groq import Groq
import os
import json
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# =========================
# 🔹 LLM CALL FUNCTION
# =========================
def ask_llm(prompt):

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()

        print("\n===== RAW LLM RESPONSE =====\n")
        print(text)

        # Clean markdown if any
        text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print("Error:", e)

        return {
            "final_verdict": "LLM parsing failed",
            "career_path": "",
            "job_fit_analysis": "",
            "evidence_based_reasoning": ""
        }


# =========================
# 🔹 PROMPT GENERATOR
# =========================
def get_analyse_prompt(
    resume_text,
    predicted_role,
    top_roles,
    achievements,
    level,
    profile_type
):

    return f"""
You are an ATS-level strict career evaluator.

RULES:
- Do NOT give generic advice
- Use ONLY provided data
- If something is missing, say "insufficient information"
- Do NOT invent skills or companies

INPUT DATA:

Resume:
{resume_text}

ML Predicted Role:
{predicted_role}

Rule-based Top Roles:
{top_roles}

Achievements:
{achievements}

Candidate Level:
{level}

Profile Type:
{profile_type}

OUTPUT FORMAT (STRICT JSON ONLY):

{{
  {
  "final_verdict": "",
  "career_path": "",
  "reasoning": [
    "point 1",
    "point 2",
    "point 3"
  ]
}
}}
"""


def get_resume_scoring_prompt(resume_text):

    return f"""
You are a resume evaluator.

Analyze the resume and return ONLY valid JSON.

Return format:

{{
    "score": 75,
    "strengths": [],
    "weaknesses": [],
    "final_suggestions": []
}}

Resume:
{resume_text}
"""