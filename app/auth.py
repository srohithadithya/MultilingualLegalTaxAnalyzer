from flask import request, session, redirect, url_for, render_template
import bcrypt

# Dummy user database
users = {"admin": bcrypt.hashpw("securepassword".encode(), bcrypt.gensalt())}

def setup_auth(app):
    @app.route('/')
    def login_page():
        if "username" in session:
            return redirect(url_for('dashboard'))
        return render_template('index.html')

    @app.route('/login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']

        if username in users and bcrypt.checkpw(password.encode(), users[username]):
            session["username"] = username
            return redirect(url_for('dashboard'))
        return render_template('index.html', error="Invalid username or password.")

    @app.route('/logout')
    def logout():
        session.pop("username", None)
        return redirect(url_for('login_page'))