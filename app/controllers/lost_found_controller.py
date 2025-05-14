from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.lost_found import LostItem
from werkzeug.utils import secure_filename
import os

lost_found_bp = Blueprint('lost_found', __name__, url_prefix='/items')


@lost_found_bp.route('/report_lost', methods=['GET', 'POST'])
@login_required
def report_lost():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        owner_name = request.form['owner_name']
        image = request.files.get('image')

        image_url = None
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(
                'app/static/uploads/item_images',
                filename)
            image.save(image_path)
            image_url = f'uploads/item_images/{filename}'

        item = LostItem(
            name=name,
            description=description,
            owner_name=owner_name,
            status='lost',
            image_url=image_url,
            reported_by=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Lost item reported.', 'success')
        return redirect(url_for('lost_found.view_items'))

    return render_template('item/report_lost.html')


@lost_found_bp.route('/report_found', methods=['GET', 'POST'])
@login_required
def report_found():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files.get('image')

        image_url = None
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join('app/static/uploads/item_images',
                                      filename)
            image.save(image_path)
            image_url = f'uploads/item_images/{filename}'

        item = LostItem(
            name=name,
            description=description,
            status='found',
            image_url=image_url,
            reported_by=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Found item reported.', 'success')
        return redirect(url_for('lost_found.view_items'))

    return render_template('item/report_found.html')


@lost_found_bp.route('/view')
@login_required
def view_items():
    items = LostItem.query.order_by(LostItem.reported_at.desc()).all()
    return render_template('item/view_items.html', items=items)
