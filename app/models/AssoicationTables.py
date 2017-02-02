from datetime import datetime
from app import db


class Characters_Traits(db.Model):
    __tablename__ = "characters_traits"

    id = db.Column(db.Integer, primary_key=True)

    trait_id = db.Column(db.Integer, db.ForeignKey('traits.id'))

    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))


class Conflicts_Traits(db.Model):
    __tablename__= "conflicts_traits"

    id = db.Column(db.Integer, primary_key=True)

    trait_id = db.Column(db.Integer, db.ForeignKey('traits.id'))

    conflict_id = db.Column(db.Integer, db.ForeignKey('conflict.id'))