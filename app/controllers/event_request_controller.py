from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.event import EventRequest, Event
from datetime import datetime

event_request_bp = Blueprint('event_request', __name__, url_prefix='/event-requests')


# Request an event (by any user)
@event_request_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event_request():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        description = request.form.get('description').strip()
        location = request.form.get('location').strip()
        event_date = request.form.get('date')

        if not title or not event_date:
            flash("Title and date are required.", "danger")
            return redirect(url_for('event_request.create_event_request'))

        new_request = EventRequest(
            user_id=current_user.id,
            title=title,
            description=description,
            location=location,
            event_date=datetime.strptime(event_date, "%Y-%m-%d %H:%M")
        )

        try:
            db.session.add(new_request)
            db.session.commit()
            flash("Event request submitted! Awaiting admin approval.", "success")
            return redirect(url_for('dashboard.home'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

    return render_template('event/request_event.html')


# Admin: View all event requests
@event_request_bp.route('/admin')
@login_required
def view_event_requests():
    if current_user.role != 'admin':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('dashboard.home'))

    requests = EventRequest.query.order_by(EventRequest.request_date.desc()).all()
    return render_template('admin/event_requests.html', requests=requests)


# Admin: Approve or deny an event request
@event_request_bp.route('/admin/<int:request_id>/<action>')
@login_required
def handle_event_request(request_id, action):
    if current_user.role != 'admin':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('dashboard.home'))

    event_request = EventRequest.query.get_or_404(request_id)

    if action == 'approve':
        # Create event in main events table
        new_event = Event(
            title=event_request.title,
            description=event_request.description,
            location=event_request.location,
            date=event_request.event_date,
            created_by=event_request.user_id
        )
        db.session.add(new_event)
        event_request.status = 'approved'

    elif action == 'deny':
        event_request.status = 'denied'

    try:
        db.session.commit()
        flash(f"Event request {action}d successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to {action} request: {str(e)}", "danger")

    return redirect(url_for('event_request.view_event_requests'))
