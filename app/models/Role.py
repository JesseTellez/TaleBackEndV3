from app import db

class Role(db.Model):
    """Class to define user roles"""

    """Not currently utilized"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))