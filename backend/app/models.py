# backend/app/models.py

from app import db # This comes from app/__init__.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json # Not strictly needed if using db.JSON, but good for clarity

class User(UserMixin, db.Model):
    __tablename__ = 'users' # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Stores the hashed password
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Use utcnow for consistency
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # Automatically updates

    # Relationships
    documents = db.relationship('Document', backref='owner', lazy=True, cascade="all, delete-orphan") # Cascade deletes documents if user is deleted

    def set_password(self, password):
        """Hashes the password and sets it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} (ID: {self.id})>'

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Link to User.id
    filename = db.Column(db.String(255), nullable=False) # Original filename
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Store raw text extracted by OCR for re-processing if needed
    raw_ocr_text = db.Column(db.Text)
    
    # Store the structured data as JSON (PostgreSQL's JSONB type is great for this)
    # This column holds the output of the data_extraction_service
    structured_data = db.Column(db.JSON) 
    
    # Path to the original uploaded file on storage (e.g., S3 URL, local path)
    storage_path = db.Column(db.String(512), nullable=False) # Ensure this is stored

    # Relationship to AnalysisResult (one-to-one)
    analysis_results = db.relationship('AnalysisResult', backref='document', lazy=True, uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Document {self.filename} (ID: {self.id}) by User {self.user_id}>'

class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), unique=True, nullable=False) # One-to-one with Document
    analyzed_data = db.Column(db.JSON, nullable=False) # The structured, refined data
    preferred_language = db.Column(db.String(10), nullable=False, default='en') # Language for output (PDF/Speech)
    pdf_report_path = db.Column(db.String(512), nullable=True) # Path to generated PDF report (if stored)
    speech_audio_path = db.Column(db.String(512), nullable=True) # Path to generated speech audio (if stored)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<AnalysisResult for Document {self.document_id} (ID: {self.id})>'


# --- Flask-Login User Loader ---
# This function is crucial for Flask-Login to load a user from the database
# based on their ID stored in the session.
from app import login_manager # Import here to avoid circular dependency (needs to be after login_manager is defined in __init__.py)

@login_manager.user_loader
def load_user(user_id):
    """Callback for Flask-Login to load a user."""
    return User.query.get(int(user_id))