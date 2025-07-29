# backend/tests/test_document_upload.py

import pytest
from flask_login import login_user
from app.models import User, Document # Assuming Document model exists
from unittest.mock import patch, MagicMock
from io import BytesIO

# Fixture to simulate a logged-in user for protected routes
@pytest.fixture
def logged_in_user_upload(app, db_session):
    with app.app_context():
        user = User(username='uploaduser', email='upload@example.com', password_hash='hashed_pass')
        db_session.add(user)
        db_session.commit()
        with app.test_request_context():
            login_user(user)
        return user

def test_document_upload_requires_login(client):
    """Test that document upload requires authentication."""
    response = client.post('/documents/upload', data={})
    assert response.status_code == 302 # Should redirect to login
    assert '/auth/login' in response.headers['Location']

@patch('app.services.ocr_service.process_document_for_ocr') # Mock the OCR service
@patch('app.services.data_extraction_service.extract_structured_data') # Mock data extraction
def test_successful_document_upload(mock_extract_data, mock_process_ocr, client, logged_in_user_upload, db_session):
    """Test that a document can be uploaded successfully."""
    # Configure mocks
    mock_process_ocr.return_value = "Extracted text from OCR and Ollama"
    mock_extract_data.return_value = {
        "invoice_number": "INV-2025-001",
        "date": "2025-07-26",
        "total_amount": "100.00",
        "currency": "INR",
        "items": []
    }

    # Create a dummy file for upload
    data = {
        'document': (BytesIO(b"dummy document content"), 'invoice.pdf', 'application/pdf')
    }
    response = client.post('/documents/upload', data=data, content_type='multipart/form-data')

    assert response.status_code == 200 # Or 201 for created
    assert response.json['message'] == 'Document uploaded and analysis initiated.'
    assert 'document_id' in response.json

    # Verify that OCR and extraction services were called
    mock_process_ocr.assert_called_once()
    mock_extract_data.assert_called_once()

    # Verify document record in database
    doc = db_session.query(Document).filter_by(filename='invoice.pdf').first()
    assert doc is not None
    assert doc.user_id == logged_in_user_upload.id
    assert doc.raw_ocr_text == "Extracted text from OCR and Ollama"
    # You might check if structured_data is populated based on mock_extract_data.return_value

def test_upload_no_file(client, logged_in_user_upload):
    """Test upload without a file."""
    response = client.post('/documents/upload', data={})
    assert response.status_code == 400
    assert response.json['message'] == 'No file part'

def test_upload_unsupported_file_type(client, logged_in_user_upload):
    """Test upload with an unsupported file type."""
    data = {
        'document': (BytesIO(b"dummy content"), 'report.doc', 'application/msword')
    }
    response = client.post('/documents/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.json['message'] == 'Unsupported file type.'

# Add more tests: direct scan (mocking camera input if applicable), large files, etc.