import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def text_to_set(text_data):
    content = " ".join(text_data) if isinstance(text_data, list) else text_data
    raw_words = re.findall(r'\b\w+\b', content.lower())
    cleaned_set = {
        w for w in raw_words 
        if w not in ENGLISH_STOP_WORDS and len(w) > 2
    }
    return cleaned_set
