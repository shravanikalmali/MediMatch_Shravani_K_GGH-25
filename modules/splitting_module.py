def split_text_ai(cleaned_text, rx_terms):
    """
    Splits the cleaned text into two sections (diagnosis and medicines) using line-level heuristics.
    
    The function splits the text by newline and then checks each line:
      - If any word in the line matches a term in the rx_terms set, the line is classified as medicine.
      - Otherwise, the line is treated as part of the diagnosis section.
    If one section is empty, it falls back to splitting the lines in half.
    
    Parameters:
      cleaned_text (str): The preprocessed text with important punctuation and newlines preserved.
      rx_terms (set): A set of RxNorm drug names (all normalized, e.g., lowercased).
      
    Returns:
      (diagnosis_text, medicines_text): A tuple of two strings.
    """
    # Split the text into non-empty lines.
    lines = [line.strip() for line in cleaned_text.split("\n") if line.strip()]
    
    # Define diagnosis-related keywords as a fallback.
    diagnosis_keywords = {"diagnosis", "symptom", "ache", "pain", "cough", "stomach", "vitals", "monitor"}
    
    diag_lines = []
    med_lines = []
    
    for line in lines:
        # Tokenize the line into words.
        words = line.split()
        # Count how many words appear in the Rx terms set.
        rx_count = sum(1 for word in words if word in rx_terms)
        # Count diagnosis keywords for additional context.
        diag_count = sum(1 for word in diagnosis_keywords if word in line)
        
        # Heuristic:
        # If at least one Rx term is found, classify this line as medicine.
        # Alternatively, if Rx count is greater than diagnosis count, consider it as medicine.
        if rx_count > 0 or (rx_count > diag_count and rx_count > 0):
            med_lines.append(line)
        else:
            diag_lines.append(line)
    
    # Fallback: if one section is empty, split lines in half.
    if not diag_lines or not med_lines:
        half = len(lines) // 2
        diag_lines = lines[:half]
        med_lines = lines[half:]
    
    diagnosis_text = "\n".join(diag_lines)
    medicines_text = "\n".join(med_lines)
    return diagnosis_text, medicines_text
