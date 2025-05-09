from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
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
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        
        # Password validation
        if password != password_confirm:
            flash("Passwords don't match!", "danger")
            return redirect(url_for('auth.register'))
        
        # Check if username exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists.", "danger")
            return redirect(url_for('auth.register'))

        # Create a new user and hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        
        # Handle role-specific fields
        role = request.form['role']
        new_user.role = role
        
        # Role-based specific data
        if role == 'student':
            new_user.school_id_number = request.form['school_id_number']
            new_user.course = request.form['course']
            new_user.year = request.form['year']
        elif role == 'faculty':
            new_user.school_id_number = request.form['school_id_number']
            new_user.department = request.form['department']
        elif role == 'others':
            new_user.phone_number = request.form['phone_number']
            legal_id_photo = request.files['legal_id_photo']
            if legal_id_photo:
                filename = secure_filename(legal_id_photo.filename)
                legal_id_photo.save(os.path.join('app/static/uploads/legal_ids', filename))
                new_user.legal_id_photo = filename

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

# Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user by username
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard.dashboard'))


        flash("Invalid username or password.", "danger")
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

# Logout Route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('auth.login'))
