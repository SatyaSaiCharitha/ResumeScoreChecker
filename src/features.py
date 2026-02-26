from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def build_tfidf_features(texts):
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(texts)
    return X, vectorizer

def save_vectorizer(vectorizer, path='src/tfidf.pkl'):
    with open(path, 'wb') as f:
        pickle.dump(vectorizer, f)