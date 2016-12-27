from datetime import datetime
from app import db
from sets import Set

__all__ = ['Story']

class Story(db.Model):
    __tablename__ = 'stories'

    '''when creating a story, you must fill out all fields that it has a foriegn relationship to...
        the story needs to know where its from/who it belongs to

        ex:
            story_ex = Story(name="test", owner=example_owner, genre=example_genre)

        to use the "many" property:
            r = Story.query.all()
            r.additions.all() -> returns all the additions

    '''
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    genre_id = db.Column(db.Integer)
    title = db.Column(db.String(200), unique=True)
    is_trending = db.Column(db.Boolean, default=False)
    unique_indicies = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    ''' backref means you create a virtual column in the addition class that references the story
        lazy - enables you to do Story.additions (returns a query that allows to search through all the additions the story has)
        ex:
    '''
    additions = db.relationship('Addition', backref='story', lazy='dynamic', cascade='all')
    #bookmarks = db.relationship('StoryVote', backref='story', lazy='dynamic')

    def to_json(self, base=None, adds=None):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'genre_id': self.genre_id,
            'title': self.title,
            'is_trending': self.is_trending,
            'number_of_additions': self.additions.count(),
            'number_of_bookmarks': self.bookmarks.count(),
            'unique_indicies_count': len(self.get_unique_indicies()),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'base': base,
            #cant just reference self.additions since jsonify does not allow arrays (security reasons)
            'active_additions':  adds
        }

    def to_feed_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'number_of_bookmarks': self.query_bookmarks
            # add number of readers
        }

    def get_unique_indicies(self):
        if self.additions <= 0:
            return 0
        index_array = []
        for add in self.additions:
            index_array.append(add.index_reference)
        return Set(index_array)

    def calculate_unique_indicies(self):
        pass

    def make_trending(self):
        pass

    def query_number_of_additions(self):
        pass


