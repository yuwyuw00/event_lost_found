from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Registration Route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        role = request.form.get('role', '').strip()

        # Validate user input
        if not username or not password or not role:
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for('auth.register'))

        if password != password_confirm:
            flash("Passwords don't match!", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for('auth.register'))

        # Create a new user instance (password will be hashed in the model)
        new_user = User(username=username, password=password, role=role)

        # Handle role-specific fields
        if role == 'student':
            new_user.school_id_number = request.form.get('school_id_number', '').strip()
            new_user.course = request.form.get('course', '').strip()
            new_user.year = request.form.get('year', '').strip()
        elif role == 'faculty':
            new_user.school_id_number = request.form.get('school_id_number', '').strip()
            new_user.department = request.form.get('department', '').strip()
        elif role == 'others':
            new_user.phone_number = request.form.get('phone_number', '').strip()
            legal_id_photo = request.files.get('legal_id_photo')
            if legal_id_photo:
                upload_folder = os.path.join('app', 'static', 'uploads', 'legal_ids')
                os.makedirs(upload_folder, exist_ok=True)
                filename = secure_filename(legal_id_photo.filename)
                legal_id_photo.save(os.path.join(upload_folder, filename))
                new_user.legal_id_photo = filename

        # Save the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {str(e)}", "danger")
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

# Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Retrieve the user by username
        user = User.query.filter_by(username=username).first()

        if user:
            # Debugging: Show stored hash and entered password (remove this in production)
            print(f"Stored hashed password: {user.password}")

            # Check password hash match
            if check_password_hash(user.password, password):
                login_user(user)
                flash("Logged in successfully!", "success")
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash("Invalid username or password.", "danger")
        else:
            flash("User not found.", "danger")

        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

# Logout Route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('auth.login'))
