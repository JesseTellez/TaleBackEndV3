#A Character is a type of story segement

from datetime import datetime
from app import db


__all__ = ['Character']

class Character(db.Model):

    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    image = db.Column(db.String(1), nullable=True)

    description = db.Column(db.Text(1000), nullable=False)

    age = db.Column(db.Integer, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    #these can be character traits and motive/resolve traits
    personal_traits = db.relationship('Trait', secondary=characters_traits, back_populates="characters")

    #belongs to many
    #premises = db.relationship('Premise', backref='characters', lazy='dynamic', cascade='all')

    owner = db.relationship('User', backref='characters', lazy='dynamic', cascade='all')

    def serialize(self, serialized_personal_traits, serialized_premises, serialized_owner):
        return {

            'id': self.id,
            'name': self.name,
            'image': self.image,
            'description': self.description,
            'age': self.age,
            'personal_traits': serialized_personal_traits,
            'owner': serialized_owner

        }




