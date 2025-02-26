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
- Python
- Google Cloud Vision API (OCR)
- Transformers (Hugging Face)
- NLTK (Natural Language Toolkit)
- Regex (Regular Expressions)
- Hugging Face Datasets
- Hugging Face Trainer API
- PyTorch
- Evaluate (Hugging Face)
- Pandas
- Data Collator with Padding (Hugging Face)
- Fuzzy Matching
- sys & os (Python Standard Library)
- [Grammar Correction Model (prithivida/grammar_error_correcter_v1)](https://huggingface.co/prithivida/grammar_error_correcter_v1)
- [Bio_ClinicalBERT (Pre-trained Model) - (emilyalsentzer/Bio_ClinicalBERT)](https://huggingface.co/emilyalsentzer/Bio_ClinicalBERT)


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


## Example run on images/prescription1.jpeg -

#### Expected Output

`Grilinctus
Dolo 650
Relent`

#### Raw OCR Data

`Shravan
21/2/2015
Tayes female
CARE
HOSPITALS
Con
Mild. Cough
Jever on
W
Stomach ache.
Ro. Typ.
Grifinitus o
Vitals
x 3 days
Rp:
103
(0) Tab. Dolo 650
P12:
50
зевар
spo₂:
Tab. Relent
"X3 day
temp: 97-0F
Adhur
4 Monitor vitals
વિ
Sujon
wear
80
a mask
U take rest for a day,`

#### Cleaned Text

`shravan<<<nl>>>21/2/2015<<<nl>>>tayes female<<<nl>>>care<<<nl>>>hospitals<<<nl>>>con<<<nl>>>mild. cough<<<nl>>>jever on<<<nl>>>w<<<nl>>>stomach ache.<<<nl>>>ro. typ.<<<nl>>>grifinitus o<<<nl>>>vitals<<<nl>>>x 3 days<<<nl>>>rp:<<<nl>>>103<<<nl>>>0 tab. dolo 650<<<nl>>>p12:<<<nl>>>50<<<nl>>> зевар<<<nl>>>spo₂:<<<nl>>>tab. relent<<<nl>>>x3 day<<<nl>>>temp: 97-0f<<<nl>>>adhur<<<nl>>>4 monitor vitals<<<nl>>>વ<<<nl>>>sujon<<<nl>>>wear<<<nl>>>80<<<nl>>>a mask<<<nl>>>u take rest for a day,`
> **Note:** The cleaned text still contains some noise, including unnecessary words and formatting artifacts (`<<<nl>>>`). Further improvements in text preprocessing are needed to refine the output by further fine-tuning the model to predict the words better.


#### Validated Medicines
`wear
  dolo 650
  vitals
  mild
  sujon
  hospitals
  tab
  relent
  typ
  spo₂
  cough
  зевар
  care
  adhur
  shravan
  p12
  con
  temp`

> **Note:** The validated medicines list includes non-medicinal terms, indicating a need for improved filtering by training the model further as the model is trained on very limited dataset currently



