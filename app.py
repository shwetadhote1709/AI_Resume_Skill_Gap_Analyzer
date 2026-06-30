import streamlit as st
import matplotlib.pyplot as plt
from ai_feedback import get_resume_feedback
from resume_parser import extract_text_from_pdf
from skills_matcher import extract_skills, skill_gap_analysis
from jd_matcher import calculate_match_score
import os

def clean_skills(skills):
    return set([s.strip().lower() for s in skills])

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="AI Resume Skill Gap Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📄 Resume Analyzer")
    st.write("🤖 AI Powered Tool")
    st.write("📊 Skill Gap Analysis")
    st.write("🎯 Resume Matching")
    st.write("📚 Career Suggestions")

# ---------------- TITLE ----------------
st.title("📄 AI Resume Skill Gap Analyzer")

# ---------------- INPUT SECTION ----------------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

st.subheader("💼 Job Description")

required_skills = [
    "python",
    "sql",
    "git",
    "github",
    "machine learning"
]

job_description = st.text_area(
    "Paste Job Description Here",
    height=200
)

# ---------------- BUTTON ----------------
if st.button("🚀 Analyze Resume"):

    # ---------- VALIDATION ----------
    if uploaded_file is None:
        st.error("⚠ Please upload resume first")
        st.stop()

    if not job_description.strip():
        st.error("⚠ Please enter Job Description")
        st.stop()

    # ---------- SAVE PDF ----------
    os.makedirs("temp", exist_ok=True)

    pdf_path = os.path.join("temp", uploaded_file.name)

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ---------- EXTRACT DATA ----------
    text = extract_text_from_pdf(pdf_path)

    with st.spinner("🤖 AI analyzing resume..."):
        ai_feedback = get_resume_feedback(text)

    resume_skills = extract_skills(text)
    jd_skills = extract_skills(job_description)

    resume_skills = clean_skills(resume_skills)
    jd_skills = clean_skills(jd_skills)

    # ---------- MATCH CALCULATION ----------
    common_skills = resume_skills.intersection(jd_skills)

    if len(jd_skills) > 0:
        jd_match_score = (len(common_skills) / len(jd_skills)) * 100
    else:
        jd_match_score = 0

    missing_skills = skill_gap_analysis(resume_skills, required_skills)

    match_score = (
        (len(required_skills) - len(missing_skills))
        / len(required_skills)
    ) * 100

    jd_missing = list(jd_skills - resume_skills)

    # ---------------- RESULTS ----------------
    st.markdown("## 🎯 Analysis Result")

    color = "#28a745" if match_score >= 80 else "#ffc107" if match_score >= 50 else "#dc3545"

    status = (
        "Excellent ✅" if match_score >= 80
        else "Good 👍" if match_score >= 50
        else "Needs Improvement ⚠"
    )

    st.markdown(
        f"""
    <div style="background:white;border:3px solid {color};border-radius:15px;padding:20px;text-align:center;box-shadow:0px 3px 10px rgba(0,0,0,0.2);">
    <h3 style="color:#333333; font-weight:bold;">🎯 ATS Resume Score</h3>
    <h1 style="color:{color};font-size:50px;">{match_score:.0f}%</h1>
    <p><b>Status:</b> {status}</p>
    </div>
    """,
        unsafe_allow_html=True
    )

    st.progress(int(match_score))

    st.markdown("---")
    st.subheader("📊 Skill Comparison Chart")

    labels = ["Found Skills", "Missing Skills"]

    values = [
        len(required_skills) - len(missing_skills),
        len(missing_skills)
    ]

    fig, ax = plt.subplots(figsize=(5, 2))   # Chart size

    ax.bar(labels, values)

    ax.set_title("Resume Skill Gap Analysis", fontsize=12)
    ax.set_ylabel("Skills", fontsize=10)

    plt.tight_layout()

    st.pyplot(fig)

    # ---------------- SKILLS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Skills Found")
        st.write(", ".join(resume_skills) if resume_skills else "None")

    with col2:
        st.subheader("⚠ Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "None")

    # ---------------- JD MATCH ----------------
    st.markdown("---")
    st.subheader("💼 Job Description Match Score")
    st.progress(int(jd_match_score))
    st.metric("JD Match Score", f"{jd_match_score}%")

    st.subheader("🚨 Missing Skills for JD")

    if jd_missing:
        for skill in jd_missing:
            st.warning(skill)
    else:
        st.success("No missing skills 🎉")

    # ---------------- RECOMMENDATIONS ----------------
    st.markdown("---")
    st.subheader("📚 Recommended Skills")

    recommendations = {
        "sql": "Learn SQL for database and analytics.",
        "github": "Learn Git & GitHub for version control.",
        "machine learning": "Start ML with Scikit-Learn."
    }

    for skill in missing_skills:
        if skill in recommendations:
            st.info(f"👉 {skill.upper()} : {recommendations[skill]}")

    # ---------------- SUMMARY ----------------
    st.markdown("---")
    st.subheader("📋 Summary")

    st.write(f"Total Resume Skills: {len(resume_skills)}")
    st.write(f"Missing Required Skills: {len(missing_skills)}")

    # ---------------- AI FEEDBACK ----------------
    st.markdown("---")
    st.subheader("🤖 AI Resume Feedback")
    st.markdown(ai_feedback)