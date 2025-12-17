from .cv_parser import extract_text_from_cv
from .ats_keywords import ROLE_KEYWORDS

def calculate_ats_score(profile):
    if not profile.cv or not profile.cv.path:
        return 0 
    cv_text = extract_text_from_cv(profile.cv.path)
    role = profile.role.lower()

    keywords = ROLE_KEYWORDS.get(role,[])
    if not keywords:
        return 50
    
    matched = 0

    for keyword in keywords:
        if keyword in cv_text:
            matched +=1

    score = (matched / len(keywords)) * 100
    return round(score,2)