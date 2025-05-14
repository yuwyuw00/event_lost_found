from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def dashboard():
    role = current_user.role

    if role == 'admin':
        return render_template(
            'pages/dashboard/admin/admin.html', user=current_user)
    elif role == 'faculty':
        return render_template(
            'pages/dashboard/faculty.html', user=current_user)
    elif role == 'student':
        return render_template(
            'pages/dashboard/student.html', user=current_user)
    elif role == 'others':
        return render_template(
            'pages/dashboard/others.html', user=current_user)
    else:
        return "Unauthorized", 403
