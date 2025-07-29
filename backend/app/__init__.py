# backend/app/__init__.py (Crucial updates)

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS # <-- Import CORS for frontend/backend communication
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables from .env file
load_dotenv()

# Initialize extensions (without app context initially)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
# Import Marshmallow after db is potentially available, or init globally if not SQLAlchemy dependent
# from app.schemas import ma # <-- Import Marshmallow instance
# Or if ma is initialized within create_app, pass app to it.
# Let's initialize ma here globally and then init_app inside create_app
from flask_marshmallow import Marshmallow
ma = Marshmallow()


def create_app(config_class=None):
    app = Flask(__name__)

    # Load configuration
    if config_class is None:
        env = os.getenv('FLASK_ENV', 'development')
        if env == 'production':
            app.config.from_object('app.config.ProductionConfig')
        elif env == 'testing':
            app.config.from_object('app.config.TestingConfig')
        else:
            app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object(config_class)

    # Load instance configuration (for local/sensitive overrides)
    app.config.from_pyfile('config.py', silent=True)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app) # Initialize Marshmallow with the app
    CORS(app) # Enable CORS for all routes by default (adjust origins as needed in production)


    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Set up basic logging (for non-production, simple console/file logging)
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(file_handler)

        app.logger.setLevel(app.config['LOG_LEVEL'])
        app.logger.info('Multi-Lingual Tax Analyzer startup')


    # Import and register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.document_upload import document_upload_bp
    from app.routes.analysis import analysis_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(document_upload_bp, url_prefix='/documents')
    app.register_blueprint(analysis_bp, url_prefix='/analysis')

    # Register Error Handlers to render templates
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    return app

# Import user_loader after create_app to prevent circular import issues if load_user uses db/models
from app.models import User
@login_manager.user_loader
def load_user(user_id):
    """Callback for Flask-Login to load a user."""
    return User.query.get(int(user_id))