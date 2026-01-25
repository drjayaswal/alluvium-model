
def generate_radar_data(matched, missing):
    CATEGORIES = {
        "Technical": ["python", "react", "fastapi", "sql", "aws", "docker", "javascript", "typescript", "api", "backend", "frontend"],
        "Soft Skills": ["leadership", "communication", "management", "teamwork", "agile", "scrum", "organized", "client"],
        "Tools": ["git", "github", "jira", "figma", "postman", "vscode", "linux", "trello"],
        "Experience": ["senior", "lead", "specialist", "professional", "years", "intermediate", "expert"]
    }
    
    radar_results = []
    
    for cat, keywords in CATEGORIES.items():
        cat_matches = [w for w in matched if w in keywords]
        cat_misses = [w for w in missing if w in keywords]
        
        total = len(cat_matches) + len(cat_misses)
        
        if total > 0:
            score = round((len(cat_matches) / total) * 100)
            radar_results.append({
                "subject": cat,
                "A": score,
                "fullMark": 100
            })
            
    if not radar_results:
        return [
            {"subject": "Overall", "A": 50, "fullMark": 100},
            {"subject": "Relevance", "A": 50, "fullMark": 100},
            {"subject": "Keywords", "A": 50, "fullMark": 100}
        ]
        
    return radar_results