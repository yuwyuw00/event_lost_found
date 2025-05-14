from flask import Blueprint, redirect, url_for, session
from flask_login import current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    if current_user.is_authenticated:  # Or: if 'user_id' in session
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))
