from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.clean import text_to_set
from app.services.types import FileData
from app.services.radar import generate_radar_data

app = FastAPI()

@app.post("/analyze")
async def analyze(data: FileData):

    input_text = " ".join(data.words)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([input_text, data.description])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    desc_set = text_to_set(data.description)
    file_set = text_to_set(data.words)
    
    full_matched = sorted(list(desc_set.intersection(file_set)))
    full_missing = sorted(list(desc_set.difference(file_set)))

    radar_data = generate_radar_data(full_matched, full_missing)

    return {
        "filename": data.filename,
        "match_score": round(float(similarity), 4),
        "status": "High Match" if similarity > 0.6 else "Low Match",
        "analysis_details": {
            "matched_keywords": full_matched[:10],
            "total_matches": len(full_matched),
            "missing_keywords": full_missing[:10],
            "total_lags": len(full_missing),
            "radar_data": radar_data,
            "summary": f"Identified {len(full_matched)} hits and {len(full_missing)} missing requirements."
        }
    }