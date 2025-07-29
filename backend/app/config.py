# backend/app/config.py

import os
from dotenv import load_dotenv
import logging # For logging configuration

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    # Flask application settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_very_insecure_default_key_for_dev_only_change_this_in_prod') # IMPORTANT: Use a strong, random key in production
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True # Enable CSRF protection (Flask-WTF for forms, if used)

    # Database settings
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Suppress warning messages

    # File Uploads (for temporary storage before OCR processing)
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 Megabytes maximum file upload size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'tiff'} # Allowed document formats

    # Ollama Vision API
    OLLAMA_API_BASE_URL = os.getenv('OLLAMA_API_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL_NAME = os.getenv('OLLAMA_MODEL_NAME', 'llava') # Default Ollama vision model

    # Google Cloud API Credentials (for Translation, Text-to-Speech if used)
    # Path to your service account key file
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    # Logging settings
    LOG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'app.log')
    LOG_LEVEL = logging.INFO

    # Celery (for background tasks like heavy OCR/analysis - future consideration)
    # CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    # CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')


class DevelopmentConfig(Config):
    """Development specific configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True # Log all database queries to console
    LOG_LEVEL = logging.DEBUG # More verbose logging in dev
    # Override UPLOAD_FOLDER for development if needed, e.g., for faster local access
    # UPLOAD_FOLDER = os.path.join(os.getcwd(), 'dev_uploads')


class ProductionConfig(Config):
    """Production specific configuration."""
    DEBUG = False
    TESTING = False
    # Ensure SECRET_KEY is set via environment variable in production deployment
    # DATABASE_URL should be a production database
    # UPLOAD_FOLDER should point to a persistent, secure storage (e.g., S3 bucket)
    # LOG_FILE should point to a production logging system
    # Consider disabling SQLALCHEMY_ECHO in production for performance
    LOG_LEVEL = logging.WARNING # Less verbose logging in production


class TestingConfig(Config):
    """Testing specific configuration."""
    TESTING = True
    DEBUG = True # Keep debug true for detailed error messages during tests
    # Use an in-memory SQLite database for fast, isolated tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Keep False for tests as well
    WTF_CSRF_ENABLED = False # Disable CSRF for easier testing of forms
    # Adjust upload folder for tests to a temporary directory if files are saved
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'test_uploads')
    LOG_LEVEL = logging.CRITICAL # Suppress most logging during tests
    OLLAMA_API_BASE_URL = "http://mock-ollama:11434" # Mock endpoint for Ollama in tests
    GOOGLE_APPLICATION_CREDENTIALS = None # Ensure no real credentials are used in tests