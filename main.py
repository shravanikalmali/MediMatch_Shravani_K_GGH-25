import os
import sys
import nltk
nltk.download('punkt_tab', quiet=True)
from modules.ocr_module import detect_text
from modules.cleaning_module import ai_clean_text
from modules.mapping_module import predict_valid_medicines
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py /path/to/your/image.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: The file '{image_path}' does not exist.")
        sys.exit(1)
    
    print("Performing OCR on image...")
    try:
        raw_text, word_boxes = detect_text(image_path)
        print("Raw OCR Text:\n", raw_text)
    except Exception as e:
        print("Error during OCR:")
        print(e)
        sys.exit(1)
    
    print("Raw OCR Text:")
    print(raw_text)
    
    # Clean the text (grammar correction disabled)
    print("\nCleaning OCR text (grammar correction disabled)...")
    cleaned_text = ai_clean_text(raw_text, use_grammar_correction=False)
    print("Cleaned Text:")
    print(cleaned_text)
    
    # Load the fine-tuned classifier.
    model = AutoModelForSequenceClassification.from_pretrained("./fine_tuned_medicine_classifier")
    tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_medicine_classifier")
    medicine_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    
    print("\nPredicting and validating medicines using the fine-tuned classifier...")
    validated_medicines = predict_valid_medicines(cleaned_text, medicine_classifier, fuzzy_threshold=80)
    print("Validated Medicines:")
    if validated_medicines:
        for med in validated_medicines:
            print(f"  {med}")
    else:
        print("  No valid medicines detected.")

if __name__ == '__main__':
    main()
