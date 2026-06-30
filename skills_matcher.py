import re

def extract_skills(text):
    skills_db = [
        "python",
        "java",
        "c",
        "c++",
        "sql",
        "html",
        "css",
        "javascript",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pandas",
        "numpy",
        "tkinter",
        "git",
        "github"
    ]

    text = text.lower()

    found_skills = []

    for skill in skills_db:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.append(skill)

    return found_skills


def skill_gap_analysis(resume_skills, required_skills):
    missing = list(set(required_skills) - set(resume_skills))
    return missing