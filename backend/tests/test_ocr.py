# backend/tests/test_ocr.py

import pytest
import os
import json
from unittest.mock import patch, MagicMock
from app.services.ocr_service import process_document_for_ocr
from app.services.data_extraction_service import extract_structured_data

# Path to your test documents
TEST_DOCS_DIR = os.path.join(os.path.dirname(__file__), 'test_documents')

# --- Fixtures for Test Data ---

@pytest.fixture
def sample_invoice_en_path():
    return os.path.join(TEST_DOCS_DIR, 'sample_invoice_en.png')

@pytest.fixture
def sample_invoice_en_expected_data():
    with open(os.path.join(TEST_DOCS_DIR, 'sample_invoice_en.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def sample_receipt_hi_path():
    return os.path.join(TEST_DOCS_DIR, 'sample_receipt_hi.pdf')

@pytest.fixture
def sample_receipt_hi_expected_data():
    with open(os.path.join(TEST_DOCS_DIR, 'sample_receipt_hi.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def crooked_invoice_path():
    return os.path.join(TEST_DOCS_DIR, 'crooked_invoice.jpg')

@pytest.fixture
def low_res_doc_path():
    return os.path.join(TEST_DOCS_DIR, 'low_res_doc.png')

@pytest.fixture
def empty_doc_path():
    return os.path.join(TEST_DOCS_DIR, 'empty_doc.pdf')

# --- Tests for ocr_service.py (Integration with Tesseract/Ollama) ---

# Note: These tests might be slower as they interact with external services.
# For CI/CD, you might mock Ollama/Tesseract, but for local integration testing,
# letting them run helps validate setup.
# If Ollama is not running, these tests will fail.

# Mocking the actual network call to Ollama.
# You'd replace this with your actual Ollama client library call
# within ocr_service.py if you had one.
@patch('requests.post') # Assuming you use 'requests' for Ollama API calls
@patch('pytesseract.image_to_string') # Mock pytesseract for speed, or let it run
def test_process_document_for_ocr_english_invoice(mock_pytesseract, mock_requests_post, sample_invoice_en_path):
    """
    Tests OCR and basic Ollama interaction for an English invoice.
    Mocks Ollama to control output for consistency.
    """
    mock_pytesseract.return_value = "Sample Company\nInvoice #INV123\nDate: 2025-07-26\nTotal: $100.00"

    # Mock Ollama Vision API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "model": "llava",
        "created_at": "2025-07-26T10:00:00.000Z",
        "response": '{"invoice_number": "INV123", "date": "2025-07-26", "total": "100.00", "currency": "$"}',
        "done": True
    }
    mock_requests_post.return_value = mock_response

    raw_text_output, ollama_json_output = process_document_for_ocr(sample_invoice_en_path, language='en')

    assert raw_text_output == "Sample Company\nInvoice #INV123\nDate: 2025-07-26\nTotal: $100.00"
    assert ollama_json_output == {"invoice_number": "INV123", "date": "2025-07-26", "total": "100.00", "currency": "$"}

    # Verify calls to external services
    mock_pytesseract.assert_called_once()
    mock_requests_post.assert_called_once()
    args, kwargs = mock_requests_post.call_args
    assert 'http://localhost:11434/api/generate' in args[0]
    assert 'llava' in kwargs['json']['model']
    assert 'image' in kwargs['json']['images'][0] # Check if image data is sent

@patch('requests.post')
@patch('pytesseract.image_to_string')
def test_process_document_for_ocr_hindi_receipt(mock_pytesseract, mock_requests_post, sample_receipt_hi_path):
    """
    Tests OCR and basic Ollama interaction for a Hindi receipt.
    Ensures language handling.
    """
    # Simulate Tesseract output for Hindi (replace with actual expected Hindi text)
    mock_pytesseract.return_value = "नमस्ते बिल\nकुल राशि: 500 रुपये" # "Hello Bill\nTotal Amount: 500 Rupees"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "model": "llava",
        "created_at": "2025-07-26T10:00:00.000Z",
        "response": '{"type": "receipt", "total_amount": "500", "currency": "INR", "language": "hi"}',
        "done": True
    }
    mock_requests_post.return_value = mock_response

    raw_text_output, ollama_json_output = process_document_for_ocr(sample_receipt_hi_path, language='hin') # Use Tesseract's lang code

    assert "नमस्ते बिल" in raw_text_output
    assert ollama_json_output['total_amount'] == "500"
    assert ollama_json_output['language'] == 'hi'
    mock_pytesseract.assert_called_once_with(
        pytest.approx(MagicMock(), rel_tol=1e-9), # Mock image object
        lang='hin', config='--psm 3' # Ensure language and psm are passed
    )
    mock_requests_post.assert_called_once()


def test_process_document_unsupported_format(empty_doc_path):
    """Test handling of unsupported document formats (e.g., empty file, corrupted)."""
    # This test might trigger exceptions from PyPDF2 or Pillow if given a truly malformed file.
    # You'd test error handling in ocr_service.py
    with pytest.raises(ValueError, match="Unsupported file type or empty document."):
        process_document_for_ocr("non_existent_file.xyz") # Or an actual unsupported file type


# --- Tests for data_extraction_service.py (Logic on processed OCR/Ollama output) ---

def test_extract_structured_data_from_ollama_output(sample_invoice_en_expected_data):
    """
    Tests the data extraction service using a mocked Ollama Vision output.
    Focuses on parsing and validation of the structured data.
    """
    # Simulate data coming directly from Ollama
    ollama_raw_output = {
        "invoice_number": "INV-XYZ-789",
        "date": "2025-06-15",
        "vendor_name": "ABC Corp.",
        "total_amount": "99.99",
        "currency": "USD",
        "gst_number": "GSTIN12345",
        "line_items_text": [
            "Item A 1 50.00",
            "Item B 2 24.99",
            "Tax 10.00"
        ]
    }
    raw_ocr_text = "This is the full raw OCR text. It contains more context."

    extracted_data = extract_structured_data(raw_ocr_text, ollama_raw_output, preferred_language='en')

    assert extracted_data['invoice_number'] == "INV-XYZ-789"
    assert extracted_data['date'] == "2025-06-15"
    assert extracted_data['vendor_name'] == "ABC Corp."
    assert float(extracted_data['total_amount']) == 99.99
    assert extracted_data['currency'] == "USD"
    assert extracted_data['gst_number'] == "GSTIN12345"
    assert len(extracted_data['line_items']) == 3 # Assuming it parses text lines into structured items
    assert extracted_data['raw_ocr_text_reference'] == raw_ocr_text[:200] # Check a snippet or hash

def test_extract_structured_data_with_missing_fields():
    """Test how data extraction handles partial or missing data from Ollama."""
    ollama_raw_output = {
        "invoice_number": "INV-TEST",
        "date": "2025-01-01",
        # Missing total_amount
    }
    raw_ocr_text = "Some text."

    extracted_data = extract_structured_data(raw_ocr_text, ollama_raw_output, preferred_language='en')

    assert extracted_data['invoice_number'] == "INV-TEST"
    assert extracted_data['date'] == "2025-01-01"
    assert extracted_data.get('total_amount') is None # Should be None or default value
    assert extracted_data.get('vendor_name') is None

def test_extract_structured_data_invalid_gst_format():
    """Test validation of GST number format."""
    ollama_raw_output = {
        "gst_number": "INVALIDGST123"
    }
    raw_ocr_text = "GST: INVALIDGST123"

    extracted_data = extract_structured_data(raw_ocr_text, ollama_raw_output, preferred_language='en')

    assert extracted_data['gst_number'] == "INVALIDGST123" # May store as is, but mark as invalid or log
    assert 'validation_errors' in extracted_data
    assert 'GST number format' in extracted_data['validation_errors']

# Add more tests for:
# - Handling different languages (e.g., Hindi specific date formats or tax IDs)
# - Error handling during processing
# - Performance with large documents
# - Accuracy metrics if you have a larger dataset of ground truth documents