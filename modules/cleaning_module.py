import re
try:
    from transformers import pipeline
    # Attempt to load a transformer-based grammar correction model.
    grammar_corrector = pipeline("text2text-generation", model="prithivida/grammar_error_correcter_v1")
except Exception as e:
    print("Warning: Could not load grammar correction model. Falling back to basic cleaning.")
    grammar_corrector = None

def ai_clean_text(raw_text, use_grammar_correction=False):
    """
    Cleans OCR text while preserving important prescription data.
    
    Parameters:
      - raw_text: The raw text string from OCR.
      - use_grammar_correction (bool): If True, apply transformer-based correction.
      
    Returns:
      - Cleaned text (str) with important punctuation and formatting preserved.
    """
    # Optionally apply transformer-based grammar correction.
    if use_grammar_correction and grammar_corrector:
        try:
            corrected = grammar_corrector(raw_text, max_length=512)
            corrected_text = corrected[0]['generated_text']
        except Exception as e:
            print("Grammar correction failed, using fallback cleaning:", e)
            corrected_text = raw_text
    else:
        corrected_text = raw_text

    # Preserve newlines by using a placeholder.
    temp_newline = "<<<NL>>>"
    text_placeholder = corrected_text.replace("\n", temp_newline)
    
    # Lowercase and normalize whitespace.
    cleaned = text_placeholder.lower().strip()
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    # More permissive regex: allow alphanumerics, whitespace, and punctuation common in prescriptions.
    # We also preserve our newline placeholder.
    cleaned = re.sub(r'[^\w\s.,:;/\-\<\>]', '', cleaned)
    
    # Restore newlines.
    cleaned = cleaned.replace(temp_newline, "\n")
    return cleaned
