from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(text):
    return model.encode([text])

def compute_similarity(resume_text, jd_text):
    resume_embedding = get_embeddings(resume_text)
    jd_embedding = get_embeddings(jd_text)

    similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
    return similarity