from app import db
from datetime import datetime
__all__ = ['AdditionVote', 'StoryVote']

#want to count the amount of distinct user_ids for a certain addition
class AdditionVote(db.Model):
    __tablename__= 'story_votes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    addition_id = db.Column(db.Integer, db.ForeignKey('additions.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class StoryVote(db.Model):
    __tablename__= 'addition_votes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
