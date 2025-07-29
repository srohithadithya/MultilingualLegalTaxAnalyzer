# backend/app/routes/dashboard.py

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models import Document, AnalysisResult
from app import db # Import the SQLAlchemy instance
from app.schemas import DocumentSchema # Import your DocumentSchema

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Initialize schemas for use in this blueprint
document_schema_list = DocumentSchema(many=True) # Use many=True for a list of documents

@dashboard_bp.route('/my_documents', methods=['GET'])
@login_required
def my_documents():
    """
    Returns a list of documents and their latest analysis results for the current user.
    """
    try:
        # Fetch documents belonging to the current user, ordered by upload date
        # Eager load analysis_results to avoid N+1 query problem if you access it repeatedly
        user_documents = db.session.query(Document).filter_by(user_id=current_user.id).order_by(Document.upload_date.desc()).all()

        # Manually add 'has_analysis' and 'summary' fields as they're not direct model fields
        # and Marshmallow's dump_only fields might not compute them directly if not set up
        # as Method fields or computed in a custom way.
        # For simplicity with the existing schema setup, let's create a list of dicts.
        documents_for_response = []
        for doc in user_documents:
            doc_data = {
                "id": doc.id,
                "filename": doc.filename,
                "upload_date": doc.upload_date.isoformat() if doc.upload_date else None,
                "has_analysis": doc.analysis_results is not None
            }
            if doc.analysis_results:
                analysis = doc.analysis_results
                doc_data["analysis_id"] = analysis.id
                doc_data["analyzed_at"] = analysis.analyzed_at.isoformat() if analysis.analyzed_at else None
                doc_data["preferred_language"] = analysis.preferred_language
                doc_data["summary"] = {
                    "invoice_number": analysis.analyzed_data.get("invoice_number"),
                    "total_amount": analysis.analyzed_data.get("total_amount"),
                    "currency": analysis.analyzed_data.get("currency"),
                    "vendor_name": analysis.analyzed_data.get("vendor_name"),
                    "date": analysis.analyzed_data.get("date")
                }
            documents_for_response.append(doc_data)

        # You could also potentially use a custom schema method or a nested schema if preferred
        # documents_data_serialized = document_schema_list.dump(user_documents)

        return jsonify({
            "message": "User dashboard data retrieved successfully",
            "username": current_user.username,
            "documents": documents_for_response # Use the manually prepared list
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error fetching dashboard data for user {current_user.id}: {e}")
        return jsonify({"message": "An error occurred while fetching dashboard data."}), 500