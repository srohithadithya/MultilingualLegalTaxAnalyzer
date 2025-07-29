# backend/app/routes/document_upload.py

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Document, AnalysisResult
from app.services.ocr_service import process_document_for_ocr
from app.services.data_extraction_service import extract_structured_data
from app.utils.validators import allowed_file_extension, generate_secure_filename # Import utilities
from app.schemas import DocumentSchema, AnalysisResultSchema # Import schemas
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

document_upload_bp = Blueprint('documents', __name__, url_prefix='/documents')

document_schema = DocumentSchema()
analysis_result_schema = AnalysisResultSchema()

@document_upload_bp.route('/upload', methods=['POST'])
@login_required
def upload_document():
    if 'document' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['document']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Use validator for allowed file types
    if not allowed_file_extension(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        return jsonify({"message": "Unsupported file type."}), 400

    original_filename = file.filename
    unique_filename = generate_secure_filename(original_filename) # Use utility to create secure filename

    # Define a temporary directory for uploaded files
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True) # Ensure directory exists
    file_path = os.path.join(upload_folder, unique_filename)

    try:
        file.save(file_path)

        # Store document info in DB immediately
        new_document = Document(
            user_id=current_user.id,
            filename=original_filename,
            storage_path=file_path # In production, this would be a cloud URL (e.g., S3)
        )
        db.session.add(new_document)
        db.session.commit()
        logger.info(f"Document {new_document.id} uploaded by user {current_user.id}")

        # --- Initiate OCR and Data Extraction ---
        # NOTE: For production, consider moving this heavy processing to a background task
        # (e.g., using Celery with Redis/RabbitMQ) to avoid blocking the web server.
        # This synchronous call is fine for development/small scale.
        try:
            raw_ocr_text, ollama_structured_output = process_document_for_ocr(
                file_path,
                language='eng', # Default initial OCR language, could auto-detect
                ollama_model=current_app.config['OLLAMA_MODEL_NAME']
            )
            extracted_data = extract_structured_data(
                raw_ocr_text,
                ollama_structured_output,
                preferred_language='en' # Default language for extraction output
            )
            logger.info(f"Document {new_document.id} OCR and data extraction completed.")

            # Update document with OCR text and structured data
            new_document.raw_ocr_text = raw_ocr_text
            new_document.structured_data = extracted_data # Store JSON data
            db.session.commit()

            # Create an initial AnalysisResult entry
            new_analysis_result = AnalysisResult(
                document_id=new_document.id,
                analyzed_data=extracted_data,
                preferred_language='en', # Default preference
                pdf_report_path=None, # Will be generated on demand
                speech_audio_path=None # Will be generated on demand
            )
            db.session.add(new_analysis_result)
            db.session.commit()
            logger.info(f"AnalysisResult {new_analysis_result.id} created for document {new_document.id}.")

            # Clean up the temporary uploaded file after successful processing
            os.remove(file_path)
            logger.info(f"Temporary file {file_path} removed.")

            return jsonify({
                "message": "Document uploaded and analysis initiated successfully.",
                "document": document_schema.dump(new_document),
                "analysis_result": analysis_result_schema.dump(new_analysis_result)
            }), 201 # Created

        except Exception as e:
            # Catch errors from OCR/Data Extraction services and rollback document
            db.session.rollback() # Rollback document creation if analysis fails
            if os.path.exists(file_path):
                os.remove(file_path) # Clean up uploaded file
            logger.error(f"Analysis failed for uploaded file {unique_filename}: {e}", exc_info=True)
            return jsonify({"message": f"Failed to process document: {e}"}), 500

    except Exception as e:
        db.session.rollback() # Ensure rollback if any error before analysis starts
        if os.path.exists(file_path): # Only if file was saved
            os.remove(file_path)
        logger.critical(f"Unexpected error during document upload or initial save: {e}", exc_info=True)
        return jsonify({"message": "An unexpected error occurred during document upload."}), 500

# @document_upload_bp.route('/scan', methods=['POST'])
# @login_required
# def scan_document():
#     # This would typically receive a base64 encoded image from the frontend webcam/scanner.
#     # The processing logic would be similar to upload_document after decoding the image data.
#     # Ensure you handle image format, size, and security.
#     return jsonify({"message": "Direct scan functionality - Not yet implemented."}), 501 # Not Implemented