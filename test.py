from resume_parser import extract_text_from_pdf
from skills_matcher import extract_skills, skill_gap_analysis

resume_path = "resumes/sample_resume.pdf"

text = extract_text_from_pdf(resume_path)

resume_skills = extract_skills(text)

required_skills = [
    "python",
    "sql",
    "git",
    "github",
    "machine learning"
]

missing_skills = skill_gap_analysis(
    resume_skills,
    required_skills
)

print("Resume Skills:")
print(resume_skills)

print("\nMissing Skills:")
print(missing_skills)