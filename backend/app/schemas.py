# backend/app/schemas.py

from flask_marshmallow import Marshmallow
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields, validate, post_load, ValidationError
from app.models import User, Document, AnalysisResult
from app.utils.security import hash_password, check_password
from datetime import datetime
import json

# Initialize Marshmallow (will be initialized in app/__init__.py)
ma = Marshmallow()

# --- Custom Validators ---
def validate_password_complexity(password):
    """
    Custom validator for password strength.
    Requires at least 8 chars, one digit, one upper, one lower, one special.
    """
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")

# --- User Schemas ---

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True # Optional: deserialize to model instances
        # Exclude sensitive fields like password_hash from being dumped (serialized)
        load_only = ("password", "confirm_password", "password_hash",) # password, confirm_password for loading only
        dump_only = ("id", "created_at",) # id and created_at for dumping only

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    # 'password' and 'confirm_password' are for input only during registration
    password = fields.String(required=True, load_only=True, validate=validate_password_complexity)
    confirm_password = fields.String(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)

    @post_load
    def validate_and_create_user(self, data, **kwargs):
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise ValidationError("Passwords do not match.", field_names=["confirm_password"])
            
            # Hash password before creating/loading instance
            data['password_hash'] = hash_password(data['password'])
            del data['password']
            del data['confirm_password']
        
        # If loading an existing instance for update, it will update directly.
        # If creating a new instance:
        if 'id' not in data and not isinstance(data.get('id'), int): # Check if it's a new user (no ID yet)
             # Basic check to prevent creating new user if an instance is somehow passed without id
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                raise ValidationError("Username already exists.", field_names=["username"])
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                raise ValidationError("Email already registered.", field_names=["email"])

        return data # Return data, let db.session.add(User(**data)) create it or load_instance handle update

class LoginSchema(ma.Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    password = fields.String(required=True)

# --- Document Schemas ---

class DocumentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        load_instance = True
        dump_only = ("id", "upload_date", "user_id",)

    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True) # User ID is set by current_user
    filename = fields.String(dump_only=True) # Filename is set during upload
    upload_date = fields.DateTime(dump_only=True)
    raw_ocr_text = fields.String(dump_only=True)
    structured_data = fields.Dict(dump_only=True) # Store as dict (JSON in DB)
    storage_path = fields.String(dump_only=True)

    # Nested schema for simplified analysis result on dashboard
    has_analysis = fields.Boolean(load_only=True) # Not a direct model field, computed
    analysis_id = fields.Integer(load_only=True) # Not a direct model field
    analyzed_at = fields.DateTime(load_only=True) # Not a direct model field
    preferred_language = fields.String(load_only=True) # Not a direct model field
    summary = fields.Dict(load_only=True) # Not a direct model field

# --- Analysis Result Schemas ---

class AnalysisResultSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AnalysisResult
        load_instance = True
        dump_only = ("id", "document_id", "analyzed_at",)
    
    id = fields.Integer(dump_only=True)
    document_id = fields.Integer(dump_only=True)
    analyzed_data = fields.Dict(required=True) # The core extracted data
    preferred_language = fields.String(required=True, validate=validate.Length(min=2, max=10))
    pdf_report_path = fields.String(dump_only=True, allow_none=True)
    speech_audio_path = fields.String(dump_only=True, allow_none=True)
    analyzed_at = fields.DateTime(dump_only=True)