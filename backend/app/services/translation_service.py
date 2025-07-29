# backend/app/services/translation_service.py

# To use Google Cloud Translation, uncomment the import and ensure GOOGLE_APPLICATION_CREDENTIALS is set
# from google.cloud import translate_v2 as translate
import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize Google Cloud Translation client if credentials are set
# try:
#     if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
#         google_translate_client = translate.Client()
#         logger.info("Google Cloud Translation client initialized.")
#     else:
#         google_translate_client = None
#         logger.warning("GOOGLE_APPLICATION_CREDENTIALS not set. Google Cloud Translation will not be used.")
# except Exception as e:
#     google_translate_client = None
#     logger.error(f"Failed to initialize Google Cloud Translation client: {e}")

def _translate_string(text, target_language):
    """Internal function to translate a single string."""
    if not text or not isinstance(text, str):
        return text # Don't translate non-strings or empty strings

    # if google_translate_client:
    #     try:
    #         result = google_translate_client.translate(text, target_language=target_language)
    #         return result['translatedText']
    #     except Exception as e:
    #         logger.error(f"Google Cloud Translation failed for '{text[:50]}...': {e}")
    #         # Fallback to dummy translation if API fails
    #         return f"Translation_Error({target_language}): {text}"
    # else:
    logger.info(f"Using dummy translation for: '{text[:50]}...' to {target_language}")
    # Dummy translation for demonstration/testing:
    return f"Translated_to_{target_language}: {text}"


def translate_text(structured_data, target_language):
    """
    Translates relevant text fields within the structured analyzed data.
    It identifies fields that are likely user-facing text and applies translation.
    """
    if not isinstance(structured_data, dict):
        logger.error("Input to translate_text must be a dictionary.")
        return structured_data # Return as is if not a dictionary

    translated_data = structured_data.copy()
    
    # Define which top-level keys should be translated
    keys_to_translate_top_level = [
        'document_type', 'vendor_name', 'vendor_address', 'customer_name',
        'customer_address', 'payment_terms', 'notes'
    ]

    for key in keys_to_translate_top_level:
        if key in translated_data and isinstance(translated_data[key], str):
            translated_data[key] = _translate_string(translated_data[key], target_language)
    
    # Translate within line_items
    if 'line_items' in translated_data and isinstance(translated_data['line_items'], list):
        translated_line_items = []
        for item in translated_data['line_items']:
            if isinstance(item, dict):
                translated_item = item.copy()
                if 'description' in translated_item and isinstance(translated_item['description'], str):
                    translated_item['description'] = _translate_string(translated_item['description'], target_language)
                # You might translate other fields within line_items if they are text
                translated_line_items.append(translated_item)
            else:
                translated_line_items.append(item) # Keep non-dict items as is
        translated_data['line_items'] = translated_line_items

    # You can add more complex translation logic here for other nested structures
    
    return translated_data