from flask_login import UserMixin
from . import db  # Relative import to avoid circular issues

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.Text, nullable=True)  # Optional bio field
    
    # Relationship with trails
    trails = db.relationship('Trail', backref='creator', lazy=True)

class Trail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    distance = db.Column(db.Float, nullable=False)  # Stored in kilometers
    scenery = db.Column(db.String(150), nullable=True)
    amenities = db.Column(db.String(150), nullable=True)
    latitude = db.Column(db.Float, nullable=False)  # New field for latitude
    longitude = db.Column(db.Float, nullable=False) # New field for longitude
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Reference to User
