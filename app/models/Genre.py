from app import db
from datetime import datetime

__all__ = ['Genre']

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    # do not need number of stories and number of active readers - just need these relationships
    description = db.Column(db.Text(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    stories = db.relationship('Story', backref='genre', lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'number_of_stories': self.query_number_of_stories,
            'number_of_active_users': self.query_number_of_active_users,
            'description': self.description,
            'updated_at': self.updated_at
        }

    # this could probably just be a property
    @classmethod
    def query_number_of_stories(self, cls):
        query = cls.query(cls.stories).count()
        if query > 0:
            return cls.query(cls.stories).count
        else:
            return 0

    def query_number_of_active_users(self):
        return 342