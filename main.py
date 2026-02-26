from src.preprocess import extract_text_from_pdf, clean_text
from src.ats_score import calculate_ats_score
from src.database import save_score

def run_pipeline(pdf_path, job_description):
    with open(pdf_path, "rb") as f:
        raw_text = extract_text_from_pdf(f)

    cleaned_resume = clean_text(raw_text)
    cleaned_jd = clean_text(job_description)

    score = calculate_ats_score(cleaned_resume, cleaned_jd)

    save_score(cleaned_resume, cleaned_jd, score)

    print(f"ATS Score: {score}/100")

if __name__ == "__main__":
    jd = input("Enter Job Description: ")
    run_pipeline("sample_resume.pdf", jd)