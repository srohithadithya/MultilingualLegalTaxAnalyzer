# backend/app/routes/auth.py

from flask import Blueprint, request, jsonify, url_for
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError # Import ValidationError
from app.models import User
from app import db # Import the SQLAlchemy instance
from app.schemas import UserSchema, LoginSchema # Import your schemas

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize schemas for use in this blueprint
user_schema = UserSchema()
login_schema = LoginSchema()

@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in", "redirect_url": url_for('dashboard.index')}), 200

    try:
        # Validate and load input data using LoginSchema
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400
    except Exception as e:
        # Catch non-JSON data or other parsing errors
        return jsonify({"message": f"Invalid request data: {e}"}), 400

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid username or password"}), 401

    login_user(user)
    
    # Handle "next" parameter for redirects after login if coming from a protected page
    next_page = request.args.get('next')
    if next_page:
        # Basic security check to prevent open redirects
        from werkzeug.urls import url_parse
        if not url_parse(next_page).netloc:
            pass # OK, it's a relative path within our domain
        else:
            next_page = None # Don't redirect to external URL

    redirect_url = next_page if next_page else url_for('dashboard.index')

    return jsonify({"message": "Logged in successfully", "redirect_url": redirect_url, "user_id": user.id}), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in", "redirect_url": url_for('dashboard.index')}), 200

    try:
        # Validate and load input data using UserSchema (which handles password hashing and matching)
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"message": "Validation Error", "errors": err.messages}), 400
    except Exception as e:
        return jsonify({"message": f"Invalid request data: {e}"}), 400

    # Marshmallow schema's @post_load already handles checking for existing user,
    # hashing password, and matching passwords.
    # If it passed load(), it means validation was successful and user data is ready.
    try:
        new_user = User(**data) # Create User instance from validated data
        db.session.add(new_user)
        db.session.commit()
        
        # Return serialized user data (without password hash)
        return jsonify({"message": "Account created successfully. Please login.", "user": user_schema.dump(new_user)}), 201
    except Exception as e:
        db.session.rollback()
        # This catch is for database errors not caught by Marshmallow's validation (e.g., unique constraint violation on DB level, though schema should prevent)
        print(f"Error during signup: {e}")
        return jsonify({"message": "An error occurred during registration. Please try again."}), 500

@auth_bp.route('/logout', methods=['POST']) # Recommend POST for logout
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route('/status', methods=['GET'])
def status():
    if current_user.is_authenticated:
        # Return serialized current user data
        return jsonify({"is_authenticated": True, "user": user_schema.dump(current_user)}), 200
    return jsonify({"is_authenticated": False, "user": None}), 200