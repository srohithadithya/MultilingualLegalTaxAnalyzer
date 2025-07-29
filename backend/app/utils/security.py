# backend/app/utils/security.py

from werkzeug.security import generate_password_hash, check_password_hash
import secrets # For generating secure tokens/keys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def hash_password(password):
    """
    Hashes a plain-text password using Werkzeug's security module (which uses PBKDF2).
    This is suitable for storing passwords securely in the database.
    """
    if not isinstance(password, str):
        logger.error("Password to hash must be a string.")
        raise TypeError("Password must be a string.")
    
    try:
        return generate_password_hash(password)
    except Exception as e:
        logger.critical(f"Error hashing password: {e}", exc_info=True)
        raise RuntimeError("Failed to hash password securely.")

def check_password(hashed_password, password):
    """
    Checks a plain-text password against a hashed password.
    Returns True if they match, False otherwise.
    """
    if not isinstance(hashed_password, str) or not isinstance(password, str):
        logger.error("Hashed password and plain password must be strings for comparison.")
        raise TypeError("Both passwords must be strings.")
    
    try:
        return check_password_hash(hashed_password, password)
    except Exception as e:
        logger.error(f"Error checking password: {e}", exc_info=True)
        # For security, return False on error rather than raising directly
        return False

def generate_secret_key(length=32):
    """
    Generates a secure, random hexadecimal string suitable for use as Flask's SECRET_KEY.
    It uses Python's secrets module for cryptographically strong random numbers.
    """
    if not isinstance(length, int) or length <= 0:
        logger.error("Length for secret key must be a positive integer.")
        raise ValueError("Length must be a positive integer.")
        
    try:
        # secrets.token_hex(nbytes) generates a string of 2*nbytes hexadecimal characters
        return secrets.token_hex(length)
    except Exception as e:
        logger.critical(f"Error generating secret key: {e}", exc_info=True)
        raise RuntimeError("Failed to generate a secure secret key.")

# Example usage (run this once to get a key for your .env):
# if __name__ == '__main__':
#     print("Generated SECRET_KEY (copy this to your .env file):")
#     print(generate_secret_key(32)) # Generates a 64-character hex string (32 bytes)