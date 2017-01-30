#A Character is a type of story segement

from datetime import datetime
from app import db

class Character(db.Model):

    __tablename__ = "story_character"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text(1000), nullable=False)

    age = db.Column(db.Integer, nullable=False)

    motive = db.Column(db.Text(1000), nullable=False)

    personal_traits = db.relationship('Traits', backref='character', lazy='dynamic', cascade='all')

    story = db.relationship('Premise', backref='character', lazy='dynamic', cascade='all')

    owner = db.relationship('User', backref='character', lazy='dynamic', cascade='all')


    #db.relationship('Addition', backref='story', lazy='dynamic', cascade='all')



