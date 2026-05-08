from phase_2 import parse_resume

def analyze_completeness(file_path):

    data = parse_resume(file_path)

    sections = {
        "education": data.get("education", "").strip(),
        "experience": data.get("experience", "").strip(),
        "projects": data.get("projects", "").strip(),
        "skills": data.get("skills", [])
    }

    status = {
        k: (len(v) > 0 if isinstance(v, list) else len(v) > 0)
        for k, v in sections.items()
    }

    score = round((sum(status.values()) / len(status)) * 100, 2)

    missing = [k for k, v in status.items() if not v]

    suggestions = []
    if "projects" in missing:
        suggestions.append("Add at least 2 projects")
    if "experience" in missing:
        suggestions.append("Add internship/work experience")
    if "education" in missing:
        suggestions.append("Add education details")
    if "skills" in missing:
        suggestions.append("Add technical skills")

    return {
        "score": score,
        "missing_sections": missing,
        "suggestions": suggestions
    }


result = analyze_completeness("Sample_3.pdf")
print(result)i