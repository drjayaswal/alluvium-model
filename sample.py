from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def analyze():
    input_text = " ".join(data.words)
    
    vectorizer = TfidfVectorizer(stop_words='english')
    
    tfidf_matrix = vectorizer.fit_transform([input_text,data.description])
    
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    return {
        "filename": data.filename,
        "match_score": round(float(similarity), 4),
        "status": "High Match" if similarity > 0.8 else "Low Match"
    }