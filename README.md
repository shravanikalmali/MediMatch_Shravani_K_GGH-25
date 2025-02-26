# MediMatch

## Overview
MediMatch is an AI-powered pharmacist’s assistant designed to extract medicine names from handwritten prescriptions using Google Vision AI OCR, classify them using a fine-tuned model, and validate them against a pharmacy’s database for order generation. This project aims to reduce manual errors and enhance pharmacy workflow efficiency.

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
