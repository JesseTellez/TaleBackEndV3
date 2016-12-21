from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db
from flask_login import UserMixin

__all__ = ['User']

class User(UserMixin, db.Model):

    """Class to represent a user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # confirmed = db.Column(db.Boolean, default=False)
    city = db.Column(db.String(254))
    bio = db.Column(db.Text(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # deal with this later
    # profile_picture_hash = db.Column(db.String(32))

    # bookmarked_additions = db.relationship('UserAdditionBookmark', foreign_keys = [UserAdditionBookmark.addition_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all')
    # bookmarked_stories = db.relationship('UserStoryBookmark', foreign_keys = [UserStoryBookmark.story_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all')
    # REFERENCE - STORY = HAS MANY (PARENT)
    stories = db.relationship("Story", backref='owner', lazy='dynamic')
    # REFERENCE - ADDITION = HAS MANY
    additions = db.relationship("Addition", lazy='dynamic')

    @property
    def serialize(self):
        """Returns object data in easily serializable format"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'city': self.city,
            'bio': self.bio,
            'created_at': self.created_at,
            'updated_at': self.updated_at
            #'stories': self.serialize_stories(),
            #'additions': self.serialize_additions()
        }

    @property
    def serialize_stories(self):
        return [story.serialize for story in self.stories]

    @property
    def serialize_addtions(self):
        return [add.serialize for add in self.additions]

    def generate_auth_token(self, app, expiration = 3000):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash.encode('utf-8'), password.encode('utf-8'))

    # For email authentication and token generations
    def generate_confirmation_token(self, expiration=3000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True