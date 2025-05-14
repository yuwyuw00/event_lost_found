#  app/controllers/item_controller.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.item import Item

item_bp = Blueprint('item', __name__, url_prefix='/item')


# View all items (lost and found)
@item_bp.route('/view', methods=['GET'])
@login_required
def view_items():
    lost_item = Item.query.filter_by(status='lost').all()
    found_item = Item.query.filter_by(status='found').all()
    return render_template(
        'item/view_items.html',
        lost_item=lost_item,
        found_item=found_item)


# Report a Lost Item
@item_bp.route('/report_lost', methods=['GET', 'POST'])
@login_required
def report_lost():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        lost_item = Item(
            name=name,
            description=description,
            status='lost',
            user_id=current_user.id)
        db.session.add(lost_item)
        db.session.commit()
        return redirect(url_for('item.view_items'))
    return render_template('item/report_lost.html')


# Report a Found Item
@item_bp.route('/report_found', methods=['GET', 'POST'])
@login_required
def report_found():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        found_item = Item(
            name=name,
            description=description,
            status='found',
            user_id=current_user.id)
        db.session.add(found_item)
        db.session.commit()
        return redirect(url_for('item.view_items'))
    return render_template('item/report_found.html')
