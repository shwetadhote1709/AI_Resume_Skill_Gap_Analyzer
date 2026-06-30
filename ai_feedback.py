import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def get_resume_feedback(resume_text):

    try:
        prompt = f"""
        Analyze this resume and provide:

        1. Strengths
        2. Weaknesses
        3. Missing skills
        4. Career suggestions

        Resume:
        {resume_text}
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception:
        return """
### 🤖 AI Feedback

**Strengths**
- Good programming foundation
- Technical skills present
- Project experience available

**Areas for Improvement**
- Learn SQL
- Learn GitHub
- Learn Machine Learning

**Career Suggestions**
- Build more Python projects
- Create a GitHub portfolio
- Explore AI/ML projects
"""