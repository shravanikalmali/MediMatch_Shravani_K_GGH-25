# MediMatch

## Overview
MediMatch is an AI-powered pharmacist’s assistant designed to extract medicine names from handwritten prescriptions using Google Vision AI OCR, classify them using a fine-tuned model, and validate them against a pharmacy’s database for order generation. This project aims to reduce manual errors and enhance pharmacy workflow efficiency.


## Installation & Setup
Clone the repository:
   `git clone https://github.com/shravanikalmali/MediMatch_Shravani_K_GGH-25.git`

Create and activate a virtual environment:
`python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate`

Install dependencies:
`pip install -r requirements.txt`

Add your credentials in the .env file

Set up Google Vision AI:
Obtain API credentials from Google Cloud Console.
Save the credentials as google_credentials.json.
Set the environment variable:
`export GOOGLE_APPLICATION_CREDENTIALS="path/to/google_credentials.json"`

Run application:
`python3 main.py path_to_prescription_image/prescription_image.png`


## Idea and Approach
After extensive research and exploring various open-source OCR toos like EasyOCR, Tesseract, Clip, etc I discovered Google lens's advancements in prescription reading. Google Lens showed promising results, so I opted for **Google Vision AI API** for text extraction from the prescription images. The raw OCR output was then preprocessed to clean and structure the extracted text. The extracted text contained both diagnoses and medications, requiring classification. To improve accuracy, I separated diagnoses from medicines and mapped identified medicines to corresponding diagnoses for validation at a later stage. To refine medicine identification, I **fine-tuned a transformer-based model** using a latest drug dataset from Kaggle. This fine-tuning enabling precise medicine name extraction. These identified medicines are then cross-checked with the pharmacy’s database for availability, enabling an automated order generation.

## Technologies Used
- **Google Vision AI API** – OCR for extracting text from handwritten prescriptions.
- **Python** – Core programming language.
- **Pandas & NumPy** – Data handling and preprocessing.
- **Regex & NLP techniques** – Text cleaning and structuring.
- **Hugging Face Transformers (Fine-tuned model)** – Classification of diagnoses and medicines.
- **CSV-based validation** – Cross-checking medicine names with pharmacy inventory.

## Workflow of MediMatch

[ Handwritten Prescription ]  
           |  
           v  
[ Google Vision AI API (OCR) ]  
           |  
           v  
[ Preprocessing (Cleaning extracted text) ]  
           |  
           v  
[ Classification (Separating Diagnosis & Medicines) ]  
           |  
           v  
[ Fine-Tuned Model (Identifying Medicine Names) ]  
           |  
           v  
[ Diagnosis-Medicine Mapping (Verifying Validity) ]  
           |  
           v  
[ Pharmacy Database Check (Matching with Inventory) ]  
           |  
           v  
[ Automated Order Generation ]  

