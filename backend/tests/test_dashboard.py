# backend/tests/test_dashboard.py

import pytest
from flask_login import login_user
from app.models import User, Document
from datetime import datetime

# Fixture to simulate a logged-in user for protected routes
@pytest.fixture
def logged_in_user(app, db_session):
    with app.app_context():
        user = User(username='loggeduser', email='logged@example.com', password_hash='hashed_pass')
        db_session.add(user)
        db_session.commit()
        # Manually log in the user using Flask-Login's login_user for testing context
        with app.test_request_context():
            login_user(user) # This will set the session

        return user

def test_dashboard_access_requires_login(client):
    """Test that the dashboard requires authentication."""
    response = client.get('/dashboard/', follow_redirects=False)
    assert response.status_code == 302 # Should redirect to login
    assert '/auth/login' in response.headers['Location']

def test_dashboard_loads_for_authenticated_user(client, logged_in_user, db_session):
    """Test that the dashboard loads and displays user's name."""
    # Since logged_in_user sets up the session, subsequent requests with client
    # in the same test function will be authenticated.
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert b"Dashboard Page" in response.data
    assert logged_in_user.username.encode('utf-8') in response.data

def test_dashboard_displays_previous_analyses(client, logged_in_user, db_session):
    """Test that the dashboard correctly lists user's documents."""
    # Add some dummy documents for the logged-in user
    doc1 = Document(user_id=logged_in_user.id, filename='invoice1.pdf', upload_date=datetime.now())
    doc2 = Document(user_id=logged_in_user.id, filename='receipt.jpg', upload_date=datetime.now())
    db_session.add_all([doc1, doc2])
    db_session.commit()

    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert b"invoice1.pdf" in response.data
    assert b"receipt.jpg" in response.data
    # You'd typically parse the HTML or JSON response more precisely here