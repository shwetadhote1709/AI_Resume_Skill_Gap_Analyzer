def calculate_match_score(resume_skills, jd_skills):

    if len(jd_skills) == 0:
        return 0

    matched = set(resume_skills).intersection(set(jd_skills))

    score = (len(matched) / len(jd_skills)) * 100

    return round(score, 2)