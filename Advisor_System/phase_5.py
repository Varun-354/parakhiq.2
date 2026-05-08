from groq import Groq
from config import API_KEY

# Initialize client
client = Groq(api_key=API_KEY)


# 🔹 Function 1: Call LLM
import json

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

        # Remove markdown formatting if present
        text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        print("Error:", e)

        return {
            "score": 50,
            "strengths": [],
            "weaknesses": ["LLM parsing failed"],
            "final_suggestions": []
        }


# 🔹 Function 2: Prompt generator
# def get_analysis_prompt(resume_text, predicted_role):

#     return f"""
# You are an expert AI Resume Advisor.

# Resume:
# {resume_text}

# Predicted Role: {predicted_role}

# Tasks:
# 1. Explain why this role fits the candidate
# 2. Identify missing or weak skills
# 3. Suggest specific improvements
# 4. Give career guidance

# Give structured output with headings.
# """


# Phase 6 

def get_analysis_prompt(resume_text, predicted_role):

    return f"""
You are an expert AI Resume Advisor.

Resume:
{resume_text}

Predicted Role: {predicted_role}

Return STRICTLY in JSON format (no extra text).

Format:
{{
  "role_fit": "string",
  "missing_skills": ["skill1", "skill2"],
  "improvements": ["improvement1", "improvement2"],
  "career_guidance": ["point1", "point2"]
}}
"""

def get_resume_scoring_prompt(resume_text):

    return f"""
You are a resume evaluator.

Analyze the resume and return ONLY valid JSON.

Do not write explanations.
Do not use markdown.
Do not use ```json

Return format:

{{
    "score": 75,
    "strengths": [
        "Good technical skills"
    ],
    "weaknesses": [
        "Projects section weak"
    ],
    "final_suggestions": [
        "Add stronger projects"
    ]
}}

Resume:
{resume_text}
"""


#Testing Code
if __name__ == "__main__":

    resume_text = "I know Python, ML, data analysis"
    predicted_role = "Data Scientist"

    prompt = get_analysis_prompt(resume_text, predicted_role)

    output = ask_llm(prompt)

    print("\n===== LLM OUTPUT =====\n")
    print(output)