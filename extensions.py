from flask import request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour"],
    headers_enabled=True,
)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return db.session.get(User, int(user_id))


@login_manager.unauthorized_handler
def handle_unauthorized():
    if request.path.startswith('/api/'):
        return jsonify({"success": False, "error": "Session expired or not logged in. Please refresh and log in again."}), 401
    return redirect(url_for('auth.login'))