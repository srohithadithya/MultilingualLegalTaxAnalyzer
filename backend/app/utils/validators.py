# backend/app/utils/validators.py

import re
import logging
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def is_valid_email(email):
    """
    Validates an email address format using a simple regex.
    More complex validation might involve checking DNS records, but this is sufficient for basic checks.
    """
    if not isinstance(email, str):
        return False
    # Regex for validating an email address (basic but covers most cases)
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None

def is_strong_password(password, min_length=8, require_digit=True, require_upper=True, require_lower=True, require_special=True):
    """
    Validates password strength based on given criteria.
    """
    if not isinstance(password, str):
        return False, "Password must be a string."

    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long."

    if require_digit and not re.search(r"\d", password):
        return False, "Password must contain at least one digit."

    if require_upper and not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if require_lower and not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if require_special and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."

    return True, "Password meets strength requirements."

def allowed_file_extension(filename, allowed_extensions):
    """
    Checks if a file's extension is in the set of allowed extensions.
    `allowed_extensions` should be a set of lowercase strings (e.g., {'png', 'jpg', 'pdf'}).
    """
    if not isinstance(filename, str) or not isinstance(allowed_extensions, set):
        logger.error("Invalid input types for allowed_file_extension.")
        return False
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_secure_filename(filename):
    """
    Generates a secure version of a filename using Werkzeug's secure_filename.
    Combines it with a UUID to ensure uniqueness.
    """
    if not isinstance(filename, str):
        logger.error("Filename must be a string.")
        raise TypeError("Filename must be a string.")
        
    import uuid # Imported here to avoid circular dependencies if utils is imported elsewhere
    try:
        # Secure the original filename to prevent directory traversal attacks
        safe_filename = secure_filename(filename)
        # Add a unique UUID prefix to prevent collisions
        unique_filename = f"{uuid.uuid4()}_{safe_filename}"
        return unique_filename
    except Exception as e:
        logger.critical(f"Error generating secure filename: {e}", exc_info=True)
        raise RuntimeError("Failed to generate a secure filename.")

# Add more validation functions as needed, e.g.,
# def is_valid_date_format(date_str, format="%Y-%m-%d"):
#     try:
#         datetime.strptime(date_str, format)
#         return True
#     except ValueError:
#         return False