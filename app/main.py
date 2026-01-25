import re
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer,ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

class FileData(BaseModel):
    filename: str
    words: List[str]
    description: str

app = FastAPI()

def clean_text_to_set(text_data):
    content = " ".join(text_data) if isinstance(text_data, list) else text_data
    raw_words = re.findall(r'\b\w+\b', content.lower())
    cleaned_set = {
        w for w in raw_words 
        if w not in ENGLISH_STOP_WORDS and len(w) > 2
    }
    return cleaned_set

@app.post("/analyze")
async def analyze(data: FileData):

    input_text = " ".join(data.words)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([input_text, data.description])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    desc_set = clean_text_to_set(data.description)
    file_set = clean_text_to_set(data.words)
    
    full_matched = sorted(list(desc_set.intersection(file_set)))
    full_missing = sorted(list(desc_set.difference(file_set)))

    return {
        "filename": data.filename,
        "match_score": round(float(similarity), 4),
        "status": "High Match" if similarity > 0.6 else "Low Match",
        "analysis_details": {
            "matched_keywords": full_matched[:10],
            "total_matches": len(full_matched),
            "missing_keywords": full_missing[:10],
            "total_lags": len(full_missing),
            "summary": f"Identified {len(full_matched)} hits and {len(full_missing)} missing requirements."
        }
    }