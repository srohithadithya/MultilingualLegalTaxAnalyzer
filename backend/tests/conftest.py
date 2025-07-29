# backend/tests/conftest.py

import pytest
from app import create_app, db, login_manager
from app.models import User, Document, AnalysisResult # Import your models
import os
from unittest.mock import patch, MagicMock

# Define a mock user loader for Flask-Login during tests
@login_manager.user_loader
def load_user(user_id):
    # In tests, we'll manually create a mock user object
    # This ensures Flask-Login works without hitting a real DB in auth tests
    mock_user = MagicMock()
    mock_user.id = int(user_id)
    mock_user.is_authenticated = True
    mock_user.is_active = True
    mock_user.is_anonymous = False
    mock_user.get_id.return_value = str(user_id)
    return mock_user

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test session."""
    # Use a testing configuration
    os.environ['FLASK_ENV'] = 'testing' # Set the environment for the app factory
    app = create_app()
    app.config.from_object('app.config.TestingConfig')

    with app.app_context():
        # Create all tables (or run migrations)
        db.create_all()
        # Optionally, if you have initial test data, load it here
        # E.g., db.session.add(User(username='testuser', ...))
        # db.session.commit()

        yield app

        # Teardown: drop all tables after tests in the session are done
        db.session.remove() # Close the session
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    """Provides a transactional database session for each test function."""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        db.session.close()
        db.session.configure(bind=connection)

        yield db.session

        # Rollback the transaction after each test to ensure a clean state
        transaction.rollback()
        connection.close()
        db.session.remove() # Clean up session