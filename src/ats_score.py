# src/ats_score.py

import re
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------------------------
# Extract Skills (simple dictionary approach)
# ---------------------------
COMMON_SKILLS = [
    "python", "java", "react", "node", "mongodb",
    "docker", "aws", "sql", "machine learning",
    "deep learning", "flask", "django", "git"
]

def extract_skills(text):
    text = text.lower()
    found = []
    for skill in COMMON_SKILLS:
        if skill in text:
            found.append(skill)
    return found


# ---------------------------
# Experience Detection
# ---------------------------
def extract_experience(text):
    matches = re.findall(r'(\d+)\s+years', text.lower())
    if matches:
        return max([int(x) for x in matches])
    return 0


# ---------------------------
# Education Detection
# ---------------------------
def education_score(text):
    text = text.lower()
    keywords = ["bachelor", "master", "phd", "b.tech", "m.tech"]
    count = sum([1 for word in keywords if word in text])
    return min(count * 20, 100)


# ---------------------------
# Project Strength
# ---------------------------
def project_score(text):
    keywords = ["project", "developed", "built", "designed", "implemented"]
    count = sum([1 for word in keywords if word in text.lower()])
    return min(count * 15, 100)


# ---------------------------
# Semantic Similarity
# ---------------------------
def semantic_similarity(resume_text, jd_text):
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(jd_text, convert_to_tensor=True)
    score = util.cos_sim(emb1, emb2).item()
    return max(score * 100, 0)


# ---------------------------
# Final ATS Score Calculation
# ---------------------------
def calculate_ats_score(resume_text, jd_text):

    semantic = semantic_similarity(resume_text, jd_text)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    skill_match = len(set(resume_skills) & set(jd_skills)) / (len(jd_skills) + 1e-5)
    skill_score = skill_match * 100

    experience = extract_experience(resume_text)
    experience_score = min(experience * 10, 100)

    edu_score = education_score(resume_text)
    proj_score = project_score(resume_text)

    overall = (
        0.4 * semantic +
        0.25 * skill_score +
        0.15 * experience_score +
        0.1 * edu_score +
        0.1 * proj_score
    )

    missing_skills = list(set(jd_skills) - set(resume_skills))

    return {
        "overall": round(overall, 2),
        "semantic": round(semantic, 2),
        "skill_score": round(skill_score, 2),
        "experience_score": round(experience_score, 2),
        "education_score": round(edu_score, 2),
        "project_score": round(proj_score, 2),
        "missing_skills": missing_skills
    }