import PyPDF2
from PIL import Image
import pytesseract
import os
import re

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        if len(text.strip()) < 50:
            print(" PDF appears to be scanned, using OCR...")
            
    except Exception as e:
        print(f" Error extracting text: {e}")
        text = f"Error: {str(e)}"
    
    return text.strip()

def extract_text_from_image(image_path: str) -> str:
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f" OCR Error: {e}")
        return f"Error: {str(e)}"

def extract_financial_data(text: str) -> dict:
    data = {
        "monthly_income": None,
        "employer_name": None,
        "account_number": None,
        "bank_name": None
    }
    
    amounts = re.findall(r'Rs\.?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', text)
    if amounts:
        amounts_cleaned = [float(amt.replace(',', '')) for amt in amounts]
        data["monthly_income"] = max(amounts_cleaned)
    
    banks = ["HBL", "UBL", "MCB", "ABL", "Standard Chartered", "Meezan", "Faysal"]
    for bank in banks:
        if bank.upper() in text.upper():
            data["bank_name"] = bank
            break
    
    account_numbers = re.findall(r'\b\d{10,20}\b', text)
    if account_numbers:
        data["account_number"] = account_numbers[0]
    
    return data

def clean_and_redact_text(text: str) -> str:
    from app.core.security import redact_pii
    return redact_pii(text)
