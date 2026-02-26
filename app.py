# main/app.py
import streamlit as st
from src.preprocess import extract_text_from_pdf, clean_text
from src.ats_score import calculate_ats_score
from src.database import save_score
import httpx
import pymongo.errors

# -------------------------
# Streamlit Page Config
# -------------------------
st.set_page_config(page_title="AI Resume ATS Checker", layout="centered")
st.title("🚀 AI Resume Intelligence System")

# -------------------------
# File Upload + Job Description
# -------------------------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Calculate ATS Score"):

    if uploaded_file and job_description:

        # -------------------------
        # 1. Extract + Clean
        # -------------------------
        try:
            raw_text = extract_text_from_pdf(uploaded_file)
            cleaned_resume = clean_text(raw_text)
            cleaned_jd = clean_text(job_description)
        except Exception as e:
            st.error(f"⚠ Error processing file: {str(e)}")
            st.stop()  # Stop execution if preprocessing fails

        # -------------------------
        # 2. Calculate Section Scores safely
        # -------------------------
        with st.spinner("Calculating ATS Score... ⏳"):
            try:
                # If your calculate_ats_score uses httpx or requests, make sure to set a timeout inside that function
                results = calculate_ats_score(cleaned_resume, cleaned_jd)
            except httpx.ReadTimeout:
                st.error("🚨 API request timed out. Please try again later.")
                st.stop()
            except Exception as e:
                st.error(f"⚠ ATS calculation failed: {str(e)}")
                st.stop()

        # -------------------------
        # 3. Save to MongoDB safely
        # -------------------------
        try:
            save_score(cleaned_resume, cleaned_jd, results["overall"])
        except pymongo.errors.PyMongoError as e:
            st.warning(f"⚠ Could not save to database: {str(e)}")

        # -------------------------
        # 4. Display Overall Score
        # -------------------------
        st.success(f"🎯 Overall ATS Score: {results['overall']}/100")

        # -------------------------
        # 5. Section Breakdown
        # -------------------------
        st.subheader("📊 Section Breakdown")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Semantic Match", f"{results.get('semantic', 0)}%")
            st.metric("Skill Match", f"{results.get('skill_score', 0)}%")
        with col2:
            st.metric("Experience Score", f"{results.get('experience_score', 0)}%")
            st.metric("Education Score", f"{results.get('education_score', 0)}%")
        st.metric("Project Strength", f"{results.get('project_score', 0)}%")

        # -------------------------
        # 6. Missing Skills
        # -------------------------
        missing_skills = results.get("missing_skills", [])
        if missing_skills:
            st.subheader("⚠ Missing Skills")
            for skill in missing_skills:
                st.write(f"- {skill}")
        else:
            st.success("No critical skill gaps detected 🎉")

        # -------------------------
        # 7. Final Recommendation
        # -------------------------
        overall = results.get("overall", 0)
        if overall > 80:
            st.info("Excellent Match! Resume highly aligned with Job Description.")
        elif overall > 60:
            st.warning("Moderate Match. Improve skills alignment and add measurable achievements.")
        else:
            st.error("Low Match. Resume needs strong customization.")

    else:
        st.warning("Please upload resume and enter job description.")