from flask import Flask
from app.routes import setup_routes
from app.auth import setup_auth

app = Flask(__name__, template_folder="app/templates")

# Load a secret key for session security

# Load the secret key from a file
with open('secret_key.txt', 'r') as f:
    app.secret_key = f.read().strip()

# Set up routes and authentication
setup_routes(app)
setup_auth(app)

if __name__ == "__main__":
    app.run(debug=True)
   