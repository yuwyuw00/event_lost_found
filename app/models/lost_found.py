from app import db

class LostItem(db.Model):
    __tablename__ = 'lost_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    owner_name = db.Column(db.String(100))
    status = db.Column(db.Enum('lost', 'found'), default='lost')
    image_url = db.Column(db.String(255))
    reported_at = db.Column(db.DateTime, server_default=db.func.now())
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'))
