from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.event import Event

from datetime import datetime

event_bp = Blueprint('event', __name__, url_prefix='/events')


# Create an Event
@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        description = request.form.get('description').strip()
        location = request.form.get('location').strip()
        date = request.form.get('date')

        if not title or not date:
            flash("Title and date are required.", "danger")
            return redirect(url_for('event.create_event'))

        new_event = Event(
            title=title,
            description=description,
            location=location,
            date=datetime.strptime(date, "%Y-%m-%dT%H:%M"),
            created_by=current_user.id
        )

        try:
            db.session.add(new_event)
            db.session.commit()
            flash("Event created successfully!", "success")
            return redirect(url_for('event.view_events'))
        except Exception as e:
            db.session.rollback()
            flash(f"Failed to create event: {str(e)}", "danger")
            return redirect(url_for('event.create_event'))

    return render_template('events/create_event.html')


# View All Events
@event_bp.route('/')
@login_required
def view_events():
    events = Event.query.all()
    return render_template('events/view_events.html', events=events)
