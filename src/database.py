# src/database.py

from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["resume_intelligence"]
collection = db["scores"]

def save_score(resume_text, jd_text, score):

    # Convert numpy float to normal Python float
    score = float(score)

    data = {
        "resume": resume_text,
        "job_description": jd_text,
        "ats_score": score,
        "created_at": datetime.utcnow()
    }

    collection.insert_one(data)