import streamlit as st
from src.preprocess import extract_text_from_pdf, clean_text
from src.ats_score import calculate_ats_score
from src.database import save_score

st.set_page_config(page_title="AI Resume ATS Checker", layout="centered")

st.title("🚀 AI Resume Intelligence System")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Calculate ATS Score"):

    if uploaded_file and job_description:

        # -------------------------
        # 1. Extract + Clean
        # -------------------------
        raw_text = extract_text_from_pdf(uploaded_file)
        cleaned_resume = clean_text(raw_text)
        cleaned_jd = clean_text(job_description)

        # -------------------------
        # 2. Calculate Section Scores
        # -------------------------
        results = calculate_ats_score(cleaned_resume, cleaned_jd)

        # -------------------------
        # 3. Save to MongoDB
        # -------------------------
        save_score(cleaned_resume, cleaned_jd, results["overall"])

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
            st.metric("Semantic Match", f"{results['semantic']}%")
            st.metric("Skill Match", f"{results['skill_score']}%")

        with col2:
            st.metric("Experience Score", f"{results['experience_score']}%")
            st.metric("Education Score", f"{results['education_score']}%")

        st.metric("Project Strength", f"{results['project_score']}%")

        # -------------------------
        # 6. Missing Skills
        # -------------------------
        if results["missing_skills"]:
            st.subheader("⚠ Missing Skills")
            for skill in results["missing_skills"]:
                st.write(f"- {skill}")
        else:
            st.success("No critical skill gaps detected 🎉")

        # -------------------------
        # 7. Final Recommendation
        # -------------------------
        if results["overall"] > 80:
            st.info("Excellent Match! Resume highly aligned with Job Description.")
        elif results["overall"] > 60:
            st.warning("Moderate Match. Improve skills alignment and add measurable achievements.")
        else:
            st.error("Low Match. Resume needs strong customization.")

    else:
        st.warning("Please upload resume and enter job description.")