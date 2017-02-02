from datetime import datetime
from app import db
from app.models.AssoicationTables import Characters_Traits as characters_traits
from app.models.AssoicationTables import Conflicts_Traits as conflicts_traits

__all__ = ['Trait']

class Trait(db.Model):

    '''Trait is a child table to Conflict and Character (Many-to-Many)'''

    __tablename__ = 'traits'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text(500), nullable=False)

    #may be able to treat it like an rgb slider
    #in the future may want this to all be held by one number and worked on that way
    wisdom_level = db.Column(db.Integer, nullable=False, default=0)

    courage_level = db.Column(db.Integer, nullable=False, default=0)

    humanity_level = db.Column(db.Integer, nullable=False, default=0)

    justice_level = db.Column(db.Integer, nullable=False, default=0)

    temperance_level = db.Column(db.Integer, nullable=False, default=0)

    trancendance_level = db.Column(db.Integer, nullable=False, default=0)

    #conflict_parents = db.relationship("Conflict", secondary=conflicts_traits, back_populates="traits")

    character_parents = db.relationship("Character", secondary="characters_traits", back_populates="personal_traits")

    def serialize(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'wisdom': self.wisdom_level,
            'courage': self.courage_level,
            'humanity': self.humanity_level,
            'justice': self.justice_level,
            'temperance': self.temperance_level,
            'trancendance': self.trancendance_level,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


