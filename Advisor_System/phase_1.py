ROLE_SKILLS = {
    "Data Analyst": [
        "python", "sql", "pandas", "excel", "statistics", "data visualization"
    ],
    "Backend Developer": [
        "python", "java", "sql", "api", "django", "flask", "databases"
    ],
    "ML Engineer": [
        "python", "machine learning", "statistics", "numpy", "model training"
    ],
    "Frontend Developer": [
        "html", "css", "javascript", "react", "ui", "responsive design"
    ],
    "DevOps Engineer": [
        "linux", "docker", "kubernetes", "ci/cd", "cloud", "aws"
    ],
    "Cyber Security Analyst": [
        "network security", "siem", "soc", "firewall",
        "ids", "ips", "threat", "vulnerability", "pentesting"
    ]
}

ALL_SKILLS = list(set(
    skill
    for skills in ROLE_SKILLS.values()
    for skill in skills
))

import re

def extract_skills_from_resume(text, skills_list):
    text = text.lower()
    found_skills = []

    for skill in skills_list:  
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))


# sample_text = """
# I have experience in Python, SQL, Machine Learning and worked with Docker and AWS.
# """

# print(extract_skills_from_resume(sample_text, ALL_SKILLS))

def get_skill_gap(extracted_skills, role):
    required_skills = ROLE_SKILLS.get(role, [])

    missing_skills = [
        skill for skill in required_skills
        if skill not in extracted_skills
    ]

    return missing_skills




# BASIC RECOMMENDATION SYSTEM
CERTIFICATION_MAP = {
    "python": "Python for Everybody - Coursera",
    "sql": "SQL for Data Science - Coursera",
    "machine learning": "Machine Learning by Andrew Ng",
    "deep learning": "Deep Learning Specialization",
    "pandas": "Data Analysis with Pandas",
    "excel": "Excel Skills for Business",
    "statistics": "Statistics for Data Science",
    "data visualization": "Tableau Data Visualization",

    "docker": "Docker Essentials",
    "aws": "AWS Certified Solutions Architect",
    "kubernetes": "Kubernetes for Beginners",

    "react": "React - The Complete Guide",
    "javascript": "JavaScript Mastery",

    "linux": "Linux Fundamentals",
}

def suggest_certifications(missing_skills):
    suggestions = []

    for skill in missing_skills:
        if skill in CERTIFICATION_MAP:
            suggestions.append(CERTIFICATION_MAP[skill])

    return list(set(suggestions))

def recommend_top_roles(extracted_skills, top_k=3):
    role_scores = []

    for role, skills in ROLE_SKILLS.items():
        match_count = len([
            skill for skill in skills
            if skill in extracted_skills
        ])

        role_scores.append((role, match_count))

    role_scores.sort(key=lambda x: x[1], reverse=True)

    return role_scores[:top_k]
