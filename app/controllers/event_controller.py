from flask import Blueprint, render_template
from flask_login import login_required

event_bp = Blueprint('events', __name__, url_prefix='/events')

# In your events_controller.py or equivalent
@event_bp.route('/request', methods=['GET', 'POST'])
def request_event():
    return render_template('events/request_event.html')

@event_bp.route('/view', methods=['GET'])
def view_events():
    return render_template('events/view_events.html')
