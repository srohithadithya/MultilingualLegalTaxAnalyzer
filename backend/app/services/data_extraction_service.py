# backend/app/services/data_extraction_service.py

import re
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def is_valid_numeric(value):
    """Checks if a string can be converted to a float."""
    if value is None:
        return False
    try:
        float(str(value).replace(',', '')) # Handle comma as thousand separator
        return True
    except ValueError:
        return False

def validate_tax_id(tax_id, country_code='IN'):
    """
    Validates a tax identification number based on country-specific patterns.
    Currently supports Indian GSTIN. Extend for other countries (VAT, EIN, ABN, etc.).
    """
    if not tax_id:
        return True, "Tax ID is empty (considered valid if not provided)." # Valid if not required or found

    tax_id = tax_id.replace(" ", "").upper() # Clean up

    if country_code == 'IN':
        # Indian GSTIN format: 15 alphanumeric characters
        # First 2 digits: State code
        # Next 10: PAN of the business (alphanumeric, 5+4+1 format)
        # 13th: Entity code (1-9 or A-Z)
        # 14th: Z (default)
        # 15th: Check digit (alphanumeric)
        gstin_pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
        if re.match(gstin_pattern, tax_id):
            return True, "Valid Indian GSTIN format."
        else:
            return False, "Invalid Indian GSTIN format."
    elif country_code == 'US':
        # US EIN (Employer Identification Number): XX-XXXXXXX (9 digits, 2-7 format)
        ein_pattern = r"^\d{2}-\d{7}$"
        if re.match(ein_pattern, tax_id):
            return True, "Valid US EIN format."
        else:
            return False, "Invalid US EIN format."
    # Add more country codes and their regex patterns here
    
    logger.info(f"No specific tax ID validation pattern for country_code: {country_code}")
    return True, "No specific validation pattern for this country." # Default if no specific rule

def normalize_date(date_str):
    """
    Attempts to parse and normalize various date string formats to YYYY-MM-DD.
    Uses a list of common formats.
    """
    if not date_str:
        return None
    
    # Clean common separators
    date_str = date_str.replace('/', '-').replace('.', '-').strip()

    # Define a list of common date formats to try
    formats = [
        '%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y', # YYYY-MM-DD, DD-MM-YYYY, MM-DD-YYYY
        '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y', # YYYY/MM/DD, DD/MM/YYYY, MM/DD/YYYY
        '%b %d, %Y', '%d %b, %Y', '%B %d, %Y', '%d %B, %Y', # Jan 01, 2025
        '%y-%m-%d', '%d-%m-%y', # YY-MM-DD (assume 20xx if YY is > 50, else 19xx)
        '%Y%m%d' # Compact format
    ]

    for fmt in formats:
        try:
            dt_obj = datetime.strptime(date_str, fmt)
            return dt_obj.strftime('%Y-%m-%d')
        except ValueError:
            pass # Try next format
    
    logger.warning(f"Could not parse and normalize date string: '{date_str}'")
    return date_str # Return original if no format matches, or None

def parse_line_items_from_text(line_items_text_list):
    """
    Attempts to parse a list of raw line item strings into structured data.
    This is highly dependent on how Ollama returns the "line_items_text".
    A robust solution might involve more advanced NLP or regex variations.
    """
    parsed_items = []
    # Regex designed to capture (description), (quantity), (unit_price), (total_price)
    # It allows for varied spacing and optional quantity/unit_price
    # Example: "Item A 2 50.00 100.00" or "Item B 200.00"
    # This is a flexible pattern. Adjust as needed for specific document types.
    line_item_pattern_full = re.compile(r"(.+?)\s+(\d+)\s+([\d.,]+)\s+([\d.,]+)$") # Desc Qty Price Total
    line_item_pattern_desc_total = re.compile(r"(.+?)\s+([\d.,]+)$") # Desc Total (e.g., if qty/unit price are missing)

    for line in line_items_text_list:
        line = line.strip()
        if not line:
            continue

        item = {"description": line, "quantity": None, "unit_price": None, "total_price": None}
        
        match_full = line_item_pattern_full.match(line)
        if match_full:
            description, quantity, unit_price, total_price = match_full.groups()
            item["description"] = description.strip()
            item["quantity"] = int(quantity) if quantity.isdigit() else quantity # Store as int if numeric
            item["unit_price"] = float(unit_price.replace(',', '')) if is_valid_numeric(unit_price) else unit_price
            item["total_price"] = float(total_price.replace(',', '')) if is_valid_numeric(total_price) else total_price
        else:
            match_desc_total = line_item_pattern_desc_total.match(line)
            if match_desc_total:
                description, total_price = match_desc_total.groups()
                item["description"] = description.strip()
                item["total_price"] = float(total_price.replace(',', '')) if is_valid_numeric(total_price) else total_price
            else:
                # If no pattern matches, keep raw description and mark for review
                logger.warning(f"Could not parse line item: '{line}'")
                item["raw_parse_fail"] = True

        parsed_items.append(item)
    return parsed_items

def extract_structured_data(raw_ocr_text, ollama_output, preferred_language='en'):
    """
    Processes raw OCR text and structured data from Ollama to extract, refine,
    and validate key tax-related information.
    """
    extracted_data = {
        "document_type": ollama_output.get("document_type"),
        "invoice_number": ollama_output.get("invoice_number"),
        "date": normalize_date(ollama_output.get("date")),
        "due_date": normalize_date(ollama_output.get("due_date")),
        "vendor_name": ollama_output.get("vendor_name"),
        "vendor_address": ollama_output.get("vendor_address"),
        "vendor_tax_id": ollama_output.get("vendor_tax_id"),
        "customer_name": ollama_output.get("customer_name"),
        "customer_address": ollama_output.get("customer_address"),
        "customer_tax_id": ollama_output.get("customer_tax_id"),
        "subtotal_amount": float(ollama_output.get("subtotal_amount", 0.0)) if is_valid_numeric(ollama_output.get("subtotal_amount")) else None,
        "tax_amount": float(ollama_output.get("tax_amount", 0.0)) if is_valid_numeric(ollama_output.get("tax_amount")) else None,
        "total_amount": float(ollama_output.get("total_amount", 0.0)) if is_valid_numeric(ollama_output.get("total_amount")) else None,
        "currency": ollama_output.get("currency"),
        "payment_terms": ollama_output.get("payment_terms"),
        "line_items": [],
        "notes": ollama_output.get("notes"),
        "extracted_language": ollama_output.get("extracted_language", preferred_language), # Use Ollama's detected lang if available
        "accuracy_confidence": ollama_output.get("accuracy_confidence"),
        "raw_ocr_text_reference": raw_ocr_text[:1000] + ("..." if len(raw_ocr_text) > 1000 else ""), # Snippet for reference
        "validation_errors": {}, # To store any validation issues
        "warnings": {} # To store non-critical warnings
    }

    # --- Validation and Refinement ---

    # Validate Tax IDs (assuming default country for now, or detect from address)
    if extracted_data.get('vendor_tax_id'):
        is_valid_gst, msg = validate_tax_id(extracted_data['vendor_tax_id'], country_code='IN') # Assuming IN for now
        if not is_valid_gst:
            extracted_data['validation_errors']['vendor_tax_id'] = msg
    
    if extracted_data.get('customer_tax_id'):
        is_valid_gst, msg = validate_tax_id(extracted_data['customer_tax_id'], country_code='IN') # Assuming IN for now
        if not is_valid_gst:
            extracted_data['validation_errors']['customer_tax_id'] = msg

    # Parse line items if Ollama provided them
    ollama_line_items = ollama_output.get('line_items')
    if ollama_line_items:
        if isinstance(ollama_line_items, list):
            # Ollama might return structured JSON directly
            if all(isinstance(item, dict) for item in ollama_line_items):
                # Assume Ollama returned a list of dicts directly
                # Perform basic type conversions if necessary
                refined_line_items = []
                for item in ollama_line_items:
                    refined_item = {
                        "description": item.get("description"),
                        "quantity": int(item["quantity"]) if isinstance(item.get("quantity"), str) and item["quantity"].isdigit() else item.get("quantity"),
                        "unit_price": float(item["unit_price"]) if is_valid_numeric(item.get("unit_price")) else item.get("unit_price"),
                        "total_price": float(item["total_price"]) if is_valid_numeric(item.get("total_price")) else item.get("total_price")
                    }
                    refined_line_items.append(refined_item)
                extracted_data['line_items'] = refined_line_items
            else:
                # Ollama returned a list but not of dicts, try parsing as raw text lines
                extracted_data['line_items'] = parse_line_items_from_text(ollama_line_items)
        elif isinstance(ollama_line_items, str):
            # If Ollama provides line items as a single string, try to split and parse
            lines = ollama_line_items.split('\n')
            extracted_data['line_items'] = parse_line_items_from_text(lines)
        else:
            logger.warning(f"Unexpected format for line_items from Ollama: {type(ollama_line_items)}")

    # --- Cross-validation (optional but highly recommended) ---
    # Example: Check if sum of line items + tax roughly equals total amount
    calculated_subtotal = sum(item.get('total_price', 0.0) for item in extracted_data['line_items'] if is_valid_numeric(item.get('total_price')))
    
    if extracted_data['total_amount'] is not None and extracted_data['subtotal_amount'] is not None and extracted_data['tax_amount'] is not None:
        if not (extracted_data['total_amount'] - (extracted_data['subtotal_amount'] + extracted_data['tax_amount'])) < 0.01: # Allow small floating point differences
            extracted_data['warnings']['total_mismatch'] = "Calculated total (subtotal + tax) does not match extracted total amount."
            logger.warning(f"Total amount mismatch for document. Extracted: {extracted_data['total_amount']}, Calculated: {extracted_data['subtotal_amount'] + extracted_data['tax_amount']}")
    elif extracted_data['total_amount'] is not None and calculated_subtotal > 0 and extracted_data['tax_amount'] is not None:
        if not (extracted_data['total_amount'] - (calculated_subtotal + extracted_data['tax_amount'])) < 0.01:
            extracted_data['warnings']['calculated_line_item_total_mismatch'] = "Calculated total from line items + tax does not match extracted total amount."
            logger.warning(f"Calculated line item total mismatch for document. Extracted: {extracted_data['total_amount']}, Calculated: {calculated_subtotal + extracted_data['tax_amount']}")

    return extracted_data