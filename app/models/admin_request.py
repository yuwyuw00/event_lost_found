from app import db


class AdminRequest(db.Model):
    __tablename__ = 'admin_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20))  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=db.func.now())
