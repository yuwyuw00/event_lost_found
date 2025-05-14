# app/models/item.py

from app import db
from datetime import datetime


class Item(db.Model):
    __tablename__ = 'items'  # The name of the table in the database

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'lost' or 'found'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    # Foreign key to associate the item with a user (who reported it)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('items', lazy=True))

    def __init__(self, name, description, status, user_id):
        self.name = name
        self.description = description
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return f"<Item {self.name} (Status: {self.status})>"

    def mark_found(self):
        """Change the status of an item to 'found'."""
        self.status = 'found'
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def mark_lost(self):
        """Change the status of an item to 'lost'."""
        self.status = 'lost'
        self.updated_at = datetime.utcnow()
        db.session.commit()
