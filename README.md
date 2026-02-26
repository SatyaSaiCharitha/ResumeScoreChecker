# Resume Score Checker (ATS Analyzer)

##  Overview
An AI-powered Resume Score Checker that evaluates resumes against job descriptions using Natural Language Processing (NLP) techniques and provides an ATS-style matching score.  
This system simulates how Applicant Tracking Systems (ATS) filter resumes based on keyword relevance and semantic similarity.

---

##  Tech Stack
- Python
- Scikit-learn
- Pandas
- NumPy
- TF-IDF Vectorization
- Cosine Similarity
- Streamlit / Flask (if used)
- MongoDB (if used)

---

##  Features
- Resume & Job Description comparison
- ATS-style scoring system
- TF-IDF based similarity calculation
- Text preprocessing pipeline
- Feature extraction module
- Modular ML architecture
- Optional database integration

---

##  Model Logic
- Resume text preprocessing
- TF-IDF vector transformation
- Cosine similarity computation
- Final ATS-style score generation

---

##  Project Structure
ResumeScoreChecker/

src/
  preprocess.py
  features.py
  embeddings.py
  ats_score.py
  model.py
  database.py
  utils.py

notebooks/
  EDA.ipynb

app.py / main.py
requirements.txt
.gitignore
README.md

---

##  How to Run

1. Install dependencies

pip install -r requirements.txt

2. Run the application

python app.py

or

python main.py

---

##  Future Improvements
- BERT-based semantic similarity
- Resume improvement suggestions
- Cloud deployment
- REST API integration

---

##  Author
Satya Sai Charitha  
Aspiring Machine Learning Engineer

