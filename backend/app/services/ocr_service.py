# backend/app/services/ocr_service.py

import pytesseract
from PIL import Image
import io
import os
import requests
import fitz # PyMuPDF for PDF handling
import base64
import json
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Set to INFO or DEBUG for more verbose output

# Get Ollama API base URL from environment variable
OLLAMA_API_BASE_URL = os.getenv('OLLAMA_API_BASE_URL', 'http://localhost:11434')

def preprocess_image(image_bytes):
    """
    Preprocesses an image for better OCR accuracy.
    This is a basic implementation. For production, consider:
    - Binarization (converting to black and white)
    - Deskewing (correcting rotation)
    - Noise reduction
    - Rescaling (upscaling low-res images)
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        # Example of basic preprocessing (uncomment and enhance as needed):
        # image = image.convert('L') # Convert to grayscale
        # image = image.point(lambda x: 0 if x < 128 else 255, '1') # Binarize
        return image
    except Exception as e:
        logger.error(f"Error during image preprocessing: {e}")
        raise ValueError(f"Could not preprocess image: {e}")

def call_ollama_vision_api(image_base64, prompt, model="llava"):
    """
    Calls the local Ollama Vision API to get structured data from an image.
    The prompt is crucial for guiding Ollama's extraction.
    """
    url = f"{OLLAMA_API_BASE_URL}/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "images": [image_base64],
        "stream": False, # We want a single, complete response
        "options": {
            "temperature": 0.1 # Low temperature for more deterministic/factual output
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=180) # Increased timeout for larger models/docs
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        full_response = response.json()
        
        # Ollama's 'response' field often contains the actual LLM output string
        llm_response_str = full_response.get('response', '')
        
        try:
            # Attempt to parse the LLM's response string as JSON.
            # Ollama might wrap JSON in markdown (e.g., ```json{...}```).
            # We need to extract the JSON part.
            if '```json' in llm_response_str and '```' in llm_response_str:
                start = llm_response_str.find('```json') + len('```json')
                end = llm_response_str.rfind('```')
                json_part = llm_response_str[start:end].strip()
                return json.loads(json_part)
            else:
                return json.loads(llm_response_str) # Assume it's direct JSON

        except json.JSONDecodeError as e:
            logger.warning(f"Ollama response not perfectly JSON: {llm_response_str}. Error: {e}")
            # If Ollama didn't return valid JSON, return its raw string response for inspection
            return {"error": "Ollama did not return valid JSON", "raw_ollama_response": llm_response_str}

    except requests.exceptions.ConnectionError as e:
        logger.error(f"ConnectionError to Ollama server at {OLLAMA_API_BASE_URL}: {e}")
        raise ConnectionError(f"Could not connect to Ollama server at {OLLAMA_API_BASE_URL}. Is it running? Error: {e}")
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout calling Ollama API at {OLLAMA_API_BASE_URL}: {e}")
        raise TimeoutError(f"Ollama API call timed out. Error: {e}")
    except requests.exceptions.RequestException as e:
        status_code = response.status_code if 'response' in locals() else 'N/A'
        response_text = response.text if 'response' in locals() else 'N/A'
        logger.error(f"Error calling Ollama API (HTTP Status: {status_code}): {e} - Response: {response_text}")
        raise Exception(f"Error calling Ollama API (Status: {status_code}): {e}")
    except Exception as e:
        logger.critical(f"An unexpected error occurred during Ollama call: {e}", exc_info=True)
        raise Exception(f"An unexpected error occurred during Ollama call: {e}")


def process_document_for_ocr(file_path, language='eng', ollama_model="llava"):
    """
    Performs OCR using Tesseract and then uses Ollama Vision for structured extraction.
    Supports images (PNG, JPG, TIFF) and PDFs.
    Returns raw OCR text and structured data (JSON) from Ollama.
    """
    raw_ocr_text = ""
    ollama_structured_data = {}
    image_base64 = None # Will store base64 of the image to send to Ollama

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.png', '.jpg', '.jpeg', '.tiff']:
        try:
            with open(file_path, 'rb') as f:
                image_bytes = f.read()
            processed_image = preprocess_image(image_bytes)
            
            # Tesseract OCR
            raw_ocr_text = pytesseract.image_to_string(processed_image, lang=language, config='--psm 3') # PSM 3 for default, auto page segmentation
            
            # Prepare image for Ollama (base64 encode)
            img_buffer = io.BytesIO()
            processed_image.save(img_buffer, format="PNG") # Save as PNG for base64 encoding
            image_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error processing image file {file_path} for OCR: {e}", exc_info=True)
            raise ValueError(f"Failed to process image file for OCR: {e}")

    elif file_extension == '.pdf':
        try:
            doc = fitz.open(file_path)
            all_text_from_pdf_pages = []
            first_page_image_bytes = None

            if doc.page_count == 0:
                raise ValueError("PDF document is empty.")

            # Process each page for full text OCR
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Render at 2x resolution for better OCR
                img_bytes = pix.tobytes("png")
                page_image = Image.open(io.BytesIO(img_bytes))

                all_text_from_pdf_pages.append(pytesseract.image_to_string(page_image, lang=language, config='--psm 3'))

                # For Ollama Vision, we'll send the first page image
                if page_num == 0:
                    first_page_image_bytes = img_bytes
                    image_base64 = base64.b64encode(first_page_image_bytes).decode('utf-8')

            raw_ocr_text = "\n".join(all_text_from_pdf_pages)
            doc.close()

        except Exception as e:
            logger.error(f"Error processing PDF file {file_path} for OCR: {e}", exc_info=True)
            raise ValueError(f"Failed to process PDF file for OCR: {e}")
    else:
        raise ValueError("Unsupported file type provided for OCR processing. Supported types: PNG, JPG, JPEG, TIFF, PDF.")

    # Call Ollama Vision if an image was successfully prepared
    if image_base64:
        # This prompt is crucial. Be specific and ask for JSON.
        # It asks for common tax-related fields. You can refine this.
        prompt = f"""
        Analyze this document (invoice, receipt, or other financial/tax document).
        Extract the following information. If a field is not present or cannot be determined, return null for that field.
        Return the information as a concise JSON object. Do not include any other text or markdown outside the JSON.

        {{
            "document_type": "string (e.g., 'invoice', 'receipt', 'bill', 'statement', 'tax_form', 'other')",
            "invoice_number": "string",
            "date": "string (YYYY-MM-DD format if possible, or original format)",
            "due_date": "string (YYYY-MM-DD format if present)",
            "vendor_name": "string (name of the company issuing the document)",
            "vendor_address": "string",
            "vendor_tax_id": "string (e.g., GSTIN, VAT ID, EIN, or null if not found)",
            "customer_name": "string (name of the recipient/customer)",
            "customer_address": "string",
            "customer_tax_id": "string (e.g., GSTIN, VAT ID, EIN, or null if not found)",
            "subtotal_amount": "string (numeric value, excluding tax)",
            "tax_amount": "string (numeric value of tax, e.g., GST/VAT)",
            "total_amount": "string (numeric value of total, including tax)",
            "currency": "string (e.g., 'USD', 'INR', '€')",
            "payment_terms": "string (e.g., 'Net 30', 'Due on receipt')",
            "line_items": [
                {{
                    "description": "string",
                    "quantity": "integer or string (if non-numeric)",
                    "unit_price": "string (numeric value)",
                    "total_price": "string (numeric value)"
                }}
                // ... more line items
            ],
            "notes": "string (any important notes or comments from the document)",
            "extracted_language": "string (ISO 639-1 code, e.g., 'en', 'hi', 'fr')",
            "accuracy_confidence": "string (e.g., 'high', 'medium', 'low' - LLM's self-assessment if possible, or leave null)",
            "error_notes": "string (any issues during extraction process by LLM)"
        }}
        """
        try:
            ollama_structured_data = call_ollama_vision_api(image_base64, prompt, model=ollama_model)
        except Exception as e:
            logger.error(f"Error during Ollama Vision API call: {e}")
            ollama_structured_data = {"error": f"Ollama processing failed: {e}"}

    return raw_ocr_text, ollama_structured_data