from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Define table name
    
    # Define columns for the users table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    school_id_number = db.Column(db.String(20), nullable=True)
    course = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    department = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    legal_id_photo = db.Column(db.String(255), nullable=True)
    
    def __init__(self, username, password, role, **kwargs):
        self.username = username
        self.set_password(password)
        self.role = role
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Method to set hashed password
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    # Method to check if password matches the hashed password
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    # You can add additional helper methods if necessary, e.g., for role checks
    def is_admin(self):
        return self.role == 'admin'

    def is_faculty(self):
        return self.role == 'faculty'

    def is_student(self):
        return self.role == 'student'

    def is_other(self):
        return self.role == 'others'
