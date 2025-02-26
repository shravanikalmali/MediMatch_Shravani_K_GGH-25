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
After extensive research, GPT-4o provided the best OCR results, but due to API limitations, I explored Google's advancements in prescription reading. Google Lens showed promising results, but as it lacks an API, I opted for **Google Vision AI API** for text extraction. The raw OCR output was preprocessed to clean and structure the extracted text. 

The extracted text contained both diagnoses and medications, requiring classification. To improve accuracy, I separated diagnoses from medicines and mapped identified medicines to corresponding diagnoses for validation. To refine medicine identification, I **fine-tuned a transformer-based model** using a **2025 drug dataset**, enabling precise medicine name extraction. These identified medicines are cross-checked with the pharmacy’s database for availability, allowing for automated order generation.

## Technologies Used
- **Google Vision AI API** – OCR for extracting text from handwritten prescriptions.
- **Python** – Core programming language.
- **Pandas & NumPy** – Data handling and preprocessing.
- **Regex & NLP techniques** – Text cleaning and structuring.
- **Hugging Face Transformers (Fine-tuned model)** – Classification of diagnoses and medicines.
- **CSV-based validation** – Cross-checking medicine names with pharmacy inventory.
- **Flask/FastAPI** – Backend API for seamless processing.

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

