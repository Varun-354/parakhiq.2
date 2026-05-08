import pickle
import re
from phase_5 import (
    ask_llm,
    get_analysis_prompt, get_resume_scoring_prompt
)
# ===== Phase 2 =====
from phase_2 import parse_resume

# ===== Phase 1 =====
from phase_1 import (
    recommend_top_roles,
    get_skill_gap,
    suggest_certifications
)


# ===== Load Model (ONLY ONCE) =====
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('tfidf.pkl', 'rb') as f:
    tfidf = pickle.load(f)


def basic_resume_score(data):
    score = 0
    strengths = []
    weaknesses = []

    # ---- Skills ----
    if data["skills"]:
        score += 25
        strengths.append("Skills section present")
    else:
        weaknesses.append("Skills section missing")

    # ---- Projects ----
    if data["projects"].strip():
        score += 25
        strengths.append("Projects section present")
    else:
        weaknesses.append("Projects section missing")

    # ---- Experience ----
    if data["experience"].strip():
        score += 25
        strengths.append("Experience present")
    else:
        weaknesses.append("Experience missing")

    # ---- Education ----
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

    strengths = (
        basic_score.get("strengths", []) +
        ai_score.get("strengths", [])
    )

    weaknesses = (
        basic_score.get("weaknesses", []) +
        ai_score.get("weaknesses", [])
    )

    suggestions = ai_score.get("final_suggestions", [])

        # ---- Score Label ----
    if final_score >= 80:
        label = "Excellent"

    elif final_score >= 60:
        label = "Good"

    elif final_score >= 40:
        label = "Average"

    else:
        label = "Needs Improvement"

    return {
        "final_score": final_score,
        "label": label,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }

# ===== MAIN PIPELINE =====
def full_resume_analysis(file_path):

    # ---- Phase 2: Parse Resume ----
    data = parse_resume(file_path)
    skills = data["skills"]


    resume_score = basic_resume_score(data)
    # ---- Phase 3: ML Prediction ----
    combined_text = (
        data["education"] + " " +
        data["experience"] + " " +
        data["projects"]
    )

    combined_text = combined_text.lower()
    combined_text = re.sub(r'[^a-z\s]', ' ', combined_text)
    combined_text = re.sub(r'\s+', ' ', combined_text).strip()

    vector = tfidf.transform([combined_text])
    predicted_role = model.predict(vector)[0]

    # ---- Phase 1: Recommendation ----
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

    resume_text =  (
    data["education"] + "\n" +
    data["experience"] + "\n" +
    data["projects"]
)

    prompt = get_analysis_prompt(resume_text, predicted_role)

    llm_feedback = ask_llm(prompt)

    score_prompt = get_resume_scoring_prompt(resume_text)
    ai_resume_score = ask_llm(score_prompt)

    print("\n===== AI RESUME SCORE =====\n")
    print(ai_resume_score)
    print(type(ai_resume_score))

    final_resume_evaluation = combine_resume_scores(
    resume_score,
    ai_resume_score
)


    # ---- Final Output ----
    return {
    "predicted_role": predicted_role,
    "skills": skills,
    "recommendations": final_output,

    "llm_feedback": {
        "role_fit": llm_feedback.get("role_fit"),
        "missing_skills": llm_feedback.get("missing_skills"),
        "improvements": llm_feedback.get("improvements"),
        "career_guidance": llm_feedback.get("career_guidance")
    },

    "final_resume_evaluation": final_resume_evaluation
}



import json

if __name__ == "__main__":
    file_path = "Sample2.pdf"   # or your file

    result = full_resume_analysis(file_path)

    print("\n===== FINAL RESULT =====\n")
    print(json.dumps(result, indent=4))