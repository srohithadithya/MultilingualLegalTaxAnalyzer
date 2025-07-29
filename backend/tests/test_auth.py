# backend/tests/test_auth.py

import pytest
from flask import url_for
from app.models import User # Make sure this import works after you define models.py
from app.utils.security import hash_password # Make sure this import works

# Fixture for a test user, ensuring a fresh user for each test
@pytest.fixture
def test_user(db_session):
    hashed_password = hash_password('password123')
    user = User(username='testuser', email='test@example.com', password_hash=hashed_password)
    db_session.add(user)
    db_session.commit()
    return user

def test_signup_page_loads(client):
    """Test that the signup page loads successfully."""
    response = client.get('/auth/signup')
    assert response.status_code == 200
    assert b"Sign Up" in response.data # Check for a string on the page

def test_successful_signup(client, db_session):
    """Test user registration."""
    data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'strongpassword',
        'confirm_password': 'strongpassword'
    }
    response = client.post('/auth/signup', data=data)
    assert response.status_code == 302 # Should redirect on success
    assert '/auth/login' in response.headers['Location'] # Redirects to login

    # Verify user is created in the database
    user = db_session.query(User).filter_by(username='newuser').first()
    assert user is not None
    assert user.email == 'new@example.com'
    assert user.check_password('strongpassword') # Assuming a check_password method on User model

def test_signup_with_existing_username(client, test_user):
    """Test registration with an already existing username."""
    data = {
        'username': test_user.username,
        'email': 'another@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }
    response = client.post('/auth/signup', data=data)
    assert response.status_code == 200 # Should render form again with error
    assert b"Username already exists." in response.data # Check for error message

def test_login_page_loads(client):
    """Test that the login page loads successfully."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_successful_login(client, test_user):
    """Test a user can successfully log in."""
    response = client.post('/auth/login', data={
        'username': test_user.username,
        'password': 'password123'
    }, follow_redirects=True) # follow_redirects to see the dashboard
    assert response.status_code == 200
    assert b"Dashboard Page" in response.data # Check for dashboard content
    # Optionally, check session for user ID or other indicators of login

def test_invalid_login_credentials(client, test_user):
    """Test login with incorrect password."""
    response = client.post('/auth/login', data={
        'username': test_user.username,
        'password': 'wrongpassword'
    })
    assert response.status_code == 200
    assert b"Invalid username or password." in response.data

def test_logout(client, test_user):
    """Test user logout."""
    # First, log in the user
    client.post('/auth/login', data={
        'username': test_user.username,
        'password': 'password123'
    })

    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data # Redirected back to login page
    # You might also check if session is cleared, though harder with test_client