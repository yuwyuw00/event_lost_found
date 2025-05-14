from flask import Blueprint, render_template, jsonify, request
from app.models.user import User
from app import db
from flask_login import current_user

admin_bp = Blueprint('admin', __name__)


# Route for the Admin Dashboard page
@admin_bp.route('/admin')
def admin_dashboard():
    return render_template('admin/admin.html')


# Route for the Manage Users HTML page
@admin_bp.route('/admin/manage_users')
def manage_users_page():
    if current_user.role != 'admin':
        return "Unauthorized", 403
    return render_template('pages/dashboard/admin/manage_users.html',
                           user=current_user)


# Route for listing all users (JSON API)
@admin_bp.route('/admin/users', methods=['GET'])
def list_users():
    users = User.query.all()
    users_data = [{
        "id": user.id,
        "name": user.name,
        "email": user.email} for user in users]
    return jsonify(users_data), 200


# Route for getting a single user (JSON)
@admin_bp.route('/admin/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_data = {"id": user.id, "name": user.name, "email": user.email}
    return jsonify(user_data), 200


# Route to create a user (JSON)
@admin_bp.route('/admin/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get('name') or not data.get('email'):
        return jsonify({"error": "Name and email are required"}), 400
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "message": "User created successfully", "user_id": new_user.id}), 201


# Route to update a user (JSON)
@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200


# Route to delete a user (JSON)
@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
