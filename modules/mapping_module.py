import re
import os
import string
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

# Use NLTK's English stopwords as a dynamic blacklist.
dynamic_blacklist = set(stopwords.words('english'))

def correct_medicine_name(token):
    """
    Normalizes the candidate token by removing any leading punctuation.
    """
    token = token.strip()
    if token.startswith("tab "):
        token = token[4:].strip()
    token_norm = token.translate(str.maketrans('', '', string.punctuation))
    return token_norm

def post_process_candidates(candidate_meds, min_length=3, max_length=30):
    """
    Applies post-processing rules to filter candidate medicine names:
      - Length filtering: Only keep candidates with length between min_length and max_length.
      - Dynamic blacklist: Discard candidates that appear in common English stopwords.
      - Numeric filtering: Discard candidates that are entirely numeric.
      - Contextual check: Only keep candidates that are either a single word or exactly two words with the second word being numeric.
     - Returns only if the candidate is a medicine name.
    Returns a set of filtered candidate medicine names.
    """
    filtered = set()
    for cand in candidate_meds:
        # Normalize: trim, lower, remove punctuation.
        cand_norm = cand.strip().lower()
        cand_norm = cand_norm.translate(str.maketrans('', '', string.punctuation))
        
        # Length filtering.
        if len(cand_norm) < min_length or len(cand_norm) > max_length:
            continue
        
        # Dynamic blacklist filtering.
        if cand_norm in dynamic_blacklist:
            continue
        
        # Discard if candidate is entirely numeric.
        if cand_norm.isdigit():
            continue
        
        filtered.add(cand_norm)
    
    # Further filter: only keep single words or exactly two words where the second is numeric.
    final_filtered = set()
    for cand in filtered:
        words = cand.split()
        if len(words) == 1:
            final_filtered.add(cand)
        elif len(words) == 2:
            # If the first token is alphabetic and the second is numeric, keep it.
            if words[0].isalpha() and words[1].isdigit():
                final_filtered.add(cand)
        # Otherwise, discard candidates with more than 2 words.
    
    return final_filtered



def predict_valid_medicines(raw_text, classifier, fuzzy_threshold=80):
    import re, string
    
    # Extract candidate tokens (any sequence of word characters)
    candidate_meds = set(re.findall(r'\b\w+(?:\s+\w+)*\b', raw_text.lower()))
    # Also extract compound phrases starting with "tab"
    compound_matches = re.findall(r'\b(tab(?:\s+\S+){1,3})\b', raw_text.lower())
    candidate_meds.update(compound_matches)
    
    validated_meds = set()
    for med in candidate_meds:
        med_clean = med.strip()
        if med_clean.startswith("tab "):
            med_clean = med_clean[4:].strip()
        med_clean_norm = med_clean.translate(str.maketrans('', '', string.punctuation))
        if len(med_clean_norm) < 3:
            continue
        result = classifier(med_clean_norm)
        if result[0]['label'] == "LABEL_1":
            validated_meds.add(med_clean_norm)
    
    from modules.mapping_module import post_process_candidates
    validated_meds = post_process_candidates(validated_meds)
    return validated_meds
