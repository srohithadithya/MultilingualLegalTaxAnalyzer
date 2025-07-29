# backend/app/routes/analysis.py

from flask import Blueprint, request, jsonify, send_file, current_app
from flask_login import login_required, current_user
from app import db # Import the SQLAlchemy instance
from app.models import Document, AnalysisResult
from app.services.translation_service import translate_text
from app.services.pdf_generation_service import generate_pdf_report
from app.services.speech_synthesis_service import generate_speech_audio
from app.schemas import AnalysisResultSchema # Import your AnalysisResultSchema
import io
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

analysis_result_schema = AnalysisResultSchema()


def get_analysis_record_and_check_ownership(document_id):
    """Helper function to get analysis record and verify user ownership."""
    analysis = db.session.query(AnalysisResult).filter_by(document_id=document_id).first()
    if not analysis:
        logger.warning(f"Analysis not found for document_id: {document_id}")
        return None, "Analysis not found for this document or it has not been analyzed yet."

    document = analysis.document # Access via relationship
    if document.user_id != current_user.id:
        logger.warning(f"User {current_user.id} attempted to access document {document_id} owned by {document.user_id}.")
        return None, "Access denied to this document."
    return analysis, None


@analysis_bp.route('/<int:document_id>', methods=['GET'])
@login_required
def get_analysis_results(document_id):
    """
    Retrieves the structured analysis results for a given document.
    """
    analysis, error_message = get_analysis_record_and_check_ownership(document_id)
    if error_message:
        status_code = 404 if "not found" in error_message else 403
        return jsonify({"message": error_message}), status_code

    try:
        # Return serialized analysis data
        return jsonify(analysis_result_schema.dump(analysis)), 200
    except Exception as e:
        logger.error(f"Error serializing analysis result for document {document_id}: {e}", exc_info=True)
        return jsonify({"message": "An error occurred while preparing analysis results."}), 500


@analysis_bp.route('/<int:document_id>/download_pdf', methods=['GET'])
@login_required
def download_pdf_report(document_id):
    """
    Generates and serves a PDF report of the analyzed data, optionally translated.
    Query parameter `lang` specifies the desired output language (e.g., ?lang=fr).
    """
    analysis, error_message = get_analysis_record_and_check_ownership(document_id)
    if error_message:
        status_code = 404 if "not found" in error_message else 403
        return jsonify({"message": error_message}), status_code

    # Get target language from query parameter, default to stored preference
    target_language = request.args.get('lang', analysis.preferred_language)
    logger.info(f"Generating PDF for document {document_id} in language {target_language}")

    try:
        # Translate the analyzed_data before PDF generation
        translated_data = translate_text(analysis.analyzed_data, target_language)
        
        pdf_buffer = generate_pdf_report(translated_data, target_language)
        
        # Update analysis record's preferred language if different (optional)
        if analysis.preferred_language != target_language:
            analysis.preferred_language = target_language
            db.session.commit()

        # Construct safe filename for download
        original_base_filename = analysis.document.filename.rsplit('.', 1)[0]
        filename = f"{original_base_filename}_{analysis.id}_{target_language}.pdf"
        
        return send_file(
            io.BytesIO(pdf_buffer),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        ), 200
    except Exception as e:
        db.session.rollback() # Rollback any potential session changes if an error occurs
        logger.error(f"Error generating PDF report for document {document_id} in {target_language}: {e}", exc_info=True)
        return jsonify({"message": "Failed to generate PDF report."}), 500


@analysis_bp.route('/<int:document_id>/speak', methods=['GET'])
@login_required
def speak_analysis(document_id):
    """
    Generates and serves an audio file (speech) of the analyzed data, optionally translated.
    Query parameter `lang` specifies the desired output language (e.g., ?lang=hi).
    """
    analysis, error_message = get_analysis_record_and_check_ownership(document_id)
    if error_message:
        status_code = 404 if "not found" in error_message else 403
        return jsonify({"message": error_message}), status_code

    target_language = request.args.get('lang', analysis.preferred_language)
    logger.info(f"Generating speech audio for document {document_id} in language {target_language}")

    try:
        # Convert structured data to a human-readable text summary for TTS
        # This summary is then translated before speech synthesis
        text_to_speak_summary = ""
        data = analysis.analyzed_data
        
        text_to_speak_summary += f"Document type: {data.get('document_type', 'N/A')}. "
        text_to_speak_summary += f"Invoice number: {data.get('invoice_number', 'N/A')}. "
        text_to_speak_summary += f"Date: {data.get('date', 'N/A')}. "
        text_to_speak_summary += f"Vendor: {data.get('vendor_name', 'N/A')}. "
        
        total_amount = data.get('total_amount')
        currency = data.get('currency', '')
        if total_amount is not None:
             text_to_speak_summary += f"Total amount: {total_amount} {currency}. "
        
        gst_number = data.get('gst_number') or data.get('vendor_tax_id')
        if gst_number:
            text_to_speak_summary += f"GST number: {gst_number}. "
        
        tax_amount = data.get('tax_amount')
        if tax_amount is not None and tax_amount > 0:
            text_to_speak_summary += f"Tax amount: {tax_amount}. "
        
        line_items = data.get('line_items')
        if line_items and isinstance(line_items, list):
            text_to_speak_summary += "Line items include: "
            for item in line_items[:3]: # Speak first few items for brevity
                desc = item.get('description', 'an item')
                qty = item.get('quantity', 'N/A')
                total = item.get('total_price', 'N/A')
                text_to_speak_summary += f"{qty} of {desc} for {total} {currency}. "

        # Translate the constructed text summary
        # Note: translate_text service can handle dicts or strings. Here we send a string.
        translated_summary_text = translate_text(text_to_speak_summary, target_language)

        audio_buffer = generate_speech_audio(translated_summary_text, target_language)
        
        # Update analysis record's preferred language if different (optional)
        if analysis.preferred_language != target_language:
            analysis.preferred_language = target_language
            db.session.commit()

        # Construct safe filename for download
        original_base_filename = analysis.document.filename.rsplit('.', 1)[0]
        filename = f"{original_base_filename}_{analysis.id}_{target_language}.mp3"

        return send_file(
            io.BytesIO(audio_buffer),
            mimetype='audio/mpeg', # Standard for MP3
            as_attachment=False, # Play directly in browser/audio player (True for download)
            download_name=filename
        ), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error generating speech audio for document {document_id} in {target_language}: {e}", exc_info=True)
        return jsonify({"message": "Failed to generate speech audio."}), 500