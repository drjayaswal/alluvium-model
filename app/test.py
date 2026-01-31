import os
import nltk
import spacy
from fastapi import FastAPI, UploadFile, File
import app.services.pre_process as extract

app = FastAPI()

try:
    nlp = spacy.load("en_core_web_md")
except:
    os.system("python -m spacy download en_core_web_md")
    nlp = spacy.load("en_core_web_md")
data_path = os.path.join(os.getcwd(), "nltk_data")
if data_path not in nltk.data.path:
    nltk.data.path.append(data_path)
for res in ['stopwords', 'punkt', 'averaged_perceptron_tagger', 'wordnet', 'omw-1.4']:
    nltk.download(res, download_dir=data_path, quiet=True)

@app.post("/get-score")
async def get_score(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    resume_raw = extract.text(await resume.read(), resume.filename)
    jd_raw = extract.text(await jd.read(), jd.filename)
    resume_info = extract.get_info(resume_raw)
    resume_processed = resume_raw.replace(".", " ")
    jd_skills, jd_noise = extract.filter_noise(jd_raw)
    res_skills, res_noise = extract.filter_noise(resume_processed)
    set_jd = set(jd_skills)
    set_res = set(res_skills)
    matched = set_jd.intersection(set_res)
    missing = set_jd - set_res
    unrelated = set_res - set_jd
    lexical_score = (len(matched) / len(set_jd)) * 100 if set_jd else 0
    doc_res = nlp(" ".join(res_skills))
    doc_jd = nlp(" ".join(jd_skills))
    semantic_score = doc_res.similarity(doc_jd) * 100 if jd_skills and res_skills else 0
    final_score = (lexical_score * 0.6) + (semantic_score * 0.4)

    return {
        "match_score": f"{round(final_score, 2)}%",
        "ml_insights": {
            "lexical_match_percent": f"{round(lexical_score, 2)}%",
            "semantic_similarity_percent": f"{round(semantic_score, 2)}%"
        },
        "resume_analysis": {
            "candidate_skills": res_skills,
            "candidate_noise_filtered": len(res_noise)
        },
        "jd_analysis": {
            "required_skills": jd_skills,
            "jd_noise_filtered": len(jd_noise)
        },
        "comparison": {
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "extra_candidate_skills": list(unrelated)
        },
        "candidate_info": resume_info
    }