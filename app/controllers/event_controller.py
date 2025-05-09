from flask import Blueprint, render_template
from flask_login import login_required

event_bp = Blueprint('events', __name__, url_prefix='/events')

# In your events_controller.py or equivalent
@events_bp.route('/request', methods=['GET', 'POST'])
def request_event():
    # Handle the event request logic here
    return render_template('events/request_event.html')
