import pickle
import re
import os

from phase_5 import ask_llm, get_resume_scoring_prompt , get_analyse_prompt
from phase_2 import parse_resume
from phase_1 import recommend_top_roles, get_skill_gap, suggest_certifications

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===== Load Model =====
with open(os.path.join(BASE_DIR, 'model.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, 'tfidf.pkl'), 'rb') as f:
    tfidf = pickle.load(f)


# =========================
# 🔹 BASIC SCORING
# =========================
def basic_resume_score(data):
    score = 0
    strengths = []
    weaknesses = []

    if data["skills"]:
        score += 25
        strengths.append("Skills section present")
    else:
        weaknesses.append("Skills section missing")

    if data["projects"].strip():
        score += 25
        strengths.append("Projects section present")
    else:
        weaknesses.append("Projects section missing")

    if data["experience"].strip():
        score += 25
        strengths.append("Experience present")
    else:
        weaknesses.append("Experience missing")

    if data["education"].strip():
        score += 25
        strengths.append("Education present")
    else:
        weaknesses.append("Education missing")

    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses
    }


# =========================
# 🔹 SCORE COMBINE
# =========================
def combine_resume_scores(basic_score, ai_score):

    if not isinstance(ai_score, dict):
        ai_score = {
            "score": 50,
            "strengths": [],
            "weaknesses": ["Invalid AI response"],
            "final_suggestions": []
        }

    final_score = int(
        (basic_score.get("score", 0) * 0.4) +
        (ai_score.get("score", 50) * 0.6)
    )

    label = (
        "Excellent" if final_score >= 80 else
        "Good" if final_score >= 60 else
        "Average" if final_score >= 40 else
        "Needs Improvement"
    )

    return {
        "final_score": final_score,
        "label": label,
        "strengths": basic_score.get("strengths", []) + ai_score.get("strengths", []),
        "weaknesses": basic_score.get("weaknesses", []) + ai_score.get("weaknesses", []),
        "suggestions": ai_score.get("final_suggestions", [])
    }


# =========================
# 🔹 MAIN PIPELINE
# =========================
def full_resume_analysis(file_path):

    data = parse_resume(file_path)
    skills = data["skills"]

    # ---- ML Prediction ----
    combined_text = (
        data["education"] + " " +
        data["experience"] + " " +
        data["projects"]
    )

    combined_text = re.sub(r'[^a-z\s]', ' ', combined_text.lower())
    vector = tfidf.transform([combined_text])
    predicted_role = model.predict(vector)[0]

    # ---- RULE BASED ----
    top_roles = recommend_top_roles(skills)

    final_output = []
    for role, score in top_roles:
        missing = get_skill_gap(skills, role)
        certs = suggest_certifications(missing)

        final_output.append({
            "role": role,
            "score": score,
            "missing_skills": missing,
            "recommendations": certs
        })

    # ---- RESUME TEXT ----
    resume_text = (
        data["education"] + "\n" +
        data["experience"] + "\n" +
        data["projects"]
    )

    # ---- BASIC SCORE ----
    resume_score = basic_resume_score(data)

    # =========================
    # 🔹 EXTRA FEATURES (FIXED LOCATION)
    # =========================
    def detect_achievements(data):
        text = (data["experience"] + data["projects"]).lower()

        achievements = {
            "internship": "low",
            "hackathon": "none",
            "company_project": "none",
            "national_level": "none"
        }

        if "intern" in text:
            achievements["internship"] = "yes"

        if "hackathon" in text:
            achievements["hackathon"] = "yes"

        if "google" in text or "amazon" in text:
            achievements["company_project"] = "high"

        return achievements

    def get_candidate_level(skills, data):
        score = 0

        if skills:
            score += 1
        if data["projects"].strip():
            score += 1
        if data["experience"].strip():
            score += 1

        return (
            "Beginner" if score <= 1 else
            "Intermediate" if score == 2 else
            "Advanced"
        )

    def get_profile_type(skills, data):
        if len(skills) > 5:
            return "Technical"
        if data["experience"].strip() and not skills:
            return "Non-Technical"
        return "Mixed"

    achievements = detect_achievements(data)
    candidate_level = get_candidate_level(skills, data)
    profile_type = get_profile_type(skills, data)

    # ---- LLM INPUT ----
    prompt = f"""
You are an expert AI career advisor.

Resume:
{resume_text}

ML Predicted Role:
{predicted_role}

Rule-based Top Roles:
{top_roles}

Achievements:
{achievements}

Candidate Level:
{candidate_level}

Profile Type:
{profile_type}

Return ONLY JSON:
{{
  "final_verdict": "",
  "career_path": "",
  "reasoning": ""
}}
"""

    llm_feedback = ask_llm(prompt)

    # ---- AI SCORE ----
    score_prompt = get_resume_scoring_prompt(resume_text)
    ai_resume_score = ask_llm(score_prompt)

    final_resume_evaluation = combine_resume_scores(
        resume_score,
        ai_resume_score
    )

    # ---- FINAL OUTPUT ----
    return {
        "predicted_role": predicted_role,
        "skills": skills,
        "recommendations": final_output,
        "achievements": achievements,
        "candidate_level": candidate_level,
        "profile_type": profile_type,
        "llm_feedback": llm_feedback,
        "final_resume_evaluation": final_resume_evaluation
    }