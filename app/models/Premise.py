from datetime import datetime
from app import db

__all__ = ['Story']

class Premise(db.Model):

    __tablename__ = 'story_premise'

    '''This class will define a story's premise - What is the foundation/base of this story?'''

    '''This will be used for stories that are formed from segments in a pool'''

    '''segments will be chosen by the owner from a pool of segments that are provided '''

    '''each premise owns a pool that will have items manually and automatically added to it'''

    id = db.Column(db.Integer, primary_key=True)
    pitch = db.Column(db.Text(400))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    segment_type = db.relationship('Segment', backref='premise', lazy='dynamic', cascade='all')
    conflicts = db.relationship('Conflict', backref='premise', lazy='dynamic', cascade='all')
    timeline = db.relationship('Setting', backref='premise', lazy='dynamic', cascade='all')
    characters = db.relationship('Character', backref='premise', lazy='dynamic', cascade='all')
    #this pool may need to be managed by redis
    pool = "Not implemented"

    def serialize(self, serialized_conflicts, serialized_timeline, serialized_characters):
        return {
            'id': self.id,
            'timeline': serialized_timeline,
            'conflicts': serialized_conflicts,
            'pitch': self.pitch,
            'characters': serialized_characters
        }
