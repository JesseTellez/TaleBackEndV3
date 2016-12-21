from app import db
from datetime import datetime

__all__ = ['Addition']

#parent ref is what points to other additions - this changes if anoter addition if the parent addition is change
#this is because the content is evaluated to see if this addition makes sense to the new context
#the index reference just ensures that the addition does not switch indexes

class Addition(db.Model):
    __tablename__ = 'additions'
    # NOTE - whenever you upvote an addition, that addition has to be re-evaluated.....checked against other additions within that story within that indexRef
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    #parent id may not be able to be null....so how do I handle the base?
    parent_id = db.Column(db.Integer, db.ForeignKey('additions.id'))
    index_reference = db.Column(db.Integer)
    '''To query the base I just have to query when the index_reference is null for a give story'''
    created_at = db.Column(db.Date, default=datetime.utcnow)
    updated_at = db.Column(db.Date, default=datetime.utcnow)

    parent_reference = db.relationship('Addition', remote_side=[id])
    bookmarks = db.relationship('AdditionVote', backref='addition', lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'parent_reference': self.parent_reference,
            # 'book_marks': self.book_marks,
            'index_reference': self.index_reference,
            'updated_at': self.updated_at
        }

    def calculate_index_ref(self):
        if self.parent_reference is not None:
            return self.parent_reference.index_reference + 1
        return 0

    def make_addition_active(self):
        # what indexref are we?
        pass