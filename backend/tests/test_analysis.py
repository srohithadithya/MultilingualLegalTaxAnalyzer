# backend/tests/test_analysis.py

import pytest
from flask_login import login_user
from app.models import User, Document, AnalysisResult
from unittest.mock import patch, MagicMock
from datetime import datetime

@pytest.fixture
def logged_in_user_analysis(app, db_session):
    with app.app_context():
        user = User(username='analysisuser', email='analysis@example.com', password_hash='hashed_pass')
        db_session.add(user)
        db_session.commit()
        with app.test_request_context():
            login_user(user)
        return user

@pytest.fixture
def analyzed_document(db_session, logged_in_user_analysis):
    doc = Document(
        user_id=logged_in_user_analysis.id,
        filename='tax_invoice.pdf',
        upload_date=datetime.now(),
        raw_ocr_text='This is raw OCR text for a tax invoice...',
        structured_data={
            "invoice_number": "TAX-2025-456",
            "date": "2025-07-20",
            "vendor_name": "Tech Solutions Pvt. Ltd.",
            "total_amount": "500.00",
            "currency": "INR",
            "gst_amount": "90.00",
            "line_items": [
                {"description": "Software License", "quantity": 1, "unit_price": "410.00", "total": "410.00"},
                {"description": "Support Fee", "quantity": 1, "unit_price": "90.00", "total": "90.00"}
            ]
        }
    )
    db_session.add(doc)
    db_session.commit()

    analysis = AnalysisResult(
        document_id=doc.id,
        analyzed_data=doc.structured_data,
        preferred_language='en', # Default for test
        pdf_report_path=f'/path/to/generated/reports/{doc.id}.pdf',
        speech_audio_path=f'/path/to/generated/audio/{doc.id}.mp3'
    )
    db_session.add(analysis)
    db_session.commit()
    return doc, analysis

def test_get_analysis_requires_login(client):
    """Test that getting analysis results requires authentication."""
    response = client.get('/analysis/1')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']

def test_get_analysis_not_found(client, logged_in_user_analysis):
    """Test getting analysis for a non-existent document."""
    response = client.get('/analysis/999')
    assert response.status_code == 404
    assert response.json['message'] == 'Analysis not found for this document or user.'

def test_get_analysis_forbidden_for_other_user(client, db_session, logged_in_user_analysis):
    """Test a user cannot access another user's analysis."""
    # Create another user and their document
    other_user = User(username='otheruser', email='other@example.com', password_hash='hashed_pass')
    db_session.add(other_user)
    db_session.commit()
    other_doc = Document(user_id=other_user.id, filename='secret_doc.pdf', upload_date=datetime.now(), structured_data={"data": "secret"})
    db_session.add(other_doc)
    db_session.commit()
    other_analysis = AnalysisResult(document_id=other_doc.id, analyzed_data=other_doc.structured_data, preferred_language='en')
    db_session.add(other_analysis)
    db_session.commit()

    response = client.get(f'/analysis/{other_doc.id}')
    assert response.status_code == 403 # Forbidden
    assert response.json['message'] == 'Access denied to this document.'

def test_get_analysis_results(client, analyzed_document):
    """Test retrieving analysis results for a valid document."""
    doc, analysis = analyzed_document
    response = client.get(f'/analysis/{doc.id}')
    assert response.status_code == 200
    assert response.json['document_id'] == doc.id
    assert response.json['analyzed_data']['invoice_number'] == "TAX-2025-456"
    assert response.json['preferred_language'] == 'en'

@patch('app.services.translation_service.translate_text')
@patch('app.services.pdf_generation_service.generate_pdf_report')
def test_download_pdf_report(mock_generate_pdf, mock_translate_text, client, analyzed_document):
    """Test downloading a generated PDF report."""
    doc, analysis = analyzed_document
    mock_generate_pdf.return_value = b"Mock PDF Content" # Simulate PDF bytes
    mock_translate_text.side_effect = lambda text, target_lang: f"Translated {text}" # Mock translation

    response = client.get(f'/analysis/{doc.id}/download_pdf?lang=fr')
    assert response.status_code == 200
    assert response.content_type == 'application/pdf'
    assert response.headers['Content-Disposition'] == f'attachment; filename=tax_invoice_{doc.id}_fr.pdf'
    assert response.data == b"Mock PDF Content"

    # Verify that the translation and PDF generation services were called
    mock_translate_text.assert_called() # Check if translation was attempted
    mock_generate_pdf.assert_called_once()
    # You can add more specific assertions on mock_generate_pdf.call_args if needed

@patch('app.services.translation_service.translate_text')
@patch('app.services.speech_synthesis_service.generate_speech_audio')
def test_get_speech_audio(mock_generate_audio, mock_translate_text, client, analyzed_document):
    """Test retrieving speech audio for analyzed data."""
    doc, analysis = analyzed_document
    mock_generate_audio.return_value = b"Mock Audio Content" # Simulate audio bytes
    mock_translate_text.side_effect = lambda text, target_lang: f"Translated {text}" # Mock translation

    response = client.get(f'/analysis/{doc.id}/speak?lang=hi')
    assert response.status_code == 200
    assert response.content_type == 'audio/mpeg' # Or appropriate audio type
    assert response.headers['Content-Disposition'] == f'attachment; filename=tax_invoice_{doc.id}_hi.mp3'
    assert response.data == b"Mock Audio Content"

    mock_translate_text.assert_called()
    mock_generate_audio.assert_called_once()

# Add tests for analysis failures (e.g., OCR error, extraction error)
# Add tests for invalid language codes