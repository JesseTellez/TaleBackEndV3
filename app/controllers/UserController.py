'''
from flask import Blueprint, request, g, jsonify, json
from .. import db
from flask_login import current_user
from sqlalchemy.sql import exists
from sqlalchemy import and_
import app.utilities as util
from app.models import Story, Addition, Vote
# define the blueprint: 'story' - set the url prefix to story
mod_story = Blueprint('story', __name__, url_prefix='/story')
#handles most sign on stuff and account stuff
'''

import json
from flask_restful import Resource, Api
from ..models.User import User as db_user
from .. import db, r
from sqlalchemy.exc import IntegrityError
from app.controllers import *
from flask_security import utils

class Login(Resource):
    """Class to handle user login route"""

    def post(self):
        """Log User In"""

        #Current App points to the application handling the request
        app = current_app._get_current_object()
        req_json = request.get_json()
        email = req_json["email"]
        password = req_json["password"]
        user = db_user.query.filter_by(email=str(email)).first()

        if user is not None:
            if utils.verify_password(password, user.password_hash):
                token = user.generate_auth_token(app)
                return jsonify({'token': token.decode('ascii')})
            else:
                return json.jsonify(error="Invalid Password!")
        else:
            return json.jsonify(error="User does not exist!")

class UserList(Resource):
    """class to handle user creation routes"""

    def post(self):
        """Create new user"""
        req_json = request.get_json()
        user = db_user()
        user.email = req_json.get("email", None)
        if user.email is None:
            msg="Must provide email!"
            return get_error_response(msg)

        user.username = req_json.get('username', None)
        password = req_json.get('password', None)
        user.city = req_json.get('city', None)
        user.bio = req_json.get('bio', None)

        if password is None:
            msg = "Must provide password"
            return get_error_response(msg)

        user.password_hash = utils.encrypt_password(password)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            msg = "Foreign key error"
            return get_error_response(msg)
        result = {
            "user": user.serialize
        }
        return get_success_response(result)

class User(Resource):
    """Class for handling fetching, updating, and deleting users"""
    def get(self, user_id):
        """Fetch user"""
        user = db_user.query.filter_by(id=str(user_id)).first()
        if user is not None:
            return get_success_response({"user": user.serialize})
        return get_error_response("User not found")

    def post(self, user_id):
        """Update User"""
        req_json = request.get_json()
        user = db_user.query.filter_by(id=str(user_id)).first()

        if user is not None:
            if len(req_json) <=0:
                result = {"user": user.serialize}
                return get_success_response(result)

        #we only want to update fields that our user requested to update

class StoryLike(Resource):
    """Class for handling Upvotes to Stories"""
    '''SO I need to use redis to cache stuff by loading it into redis first and then checking redis from then on out'''
    '''I need to use redis pubsub for the act of providing the app with responsiveness'''
    '''issue:  Do I use redis to save all the likes for the user or do I use it to relay calls to the db?'''
    '''Likes are a relational thing so I dont feel that they should be in redis'''
    def post(self):
        """upvote a story"""
        req_json = request.get_json()
        user_id = req_json["user_id"]
        story_id = req_json["story_id"]
        message = 'user {user} upvoted: story {story}'.format(user=user_id, story=story_id)
        channel = 'LikeChannel'
        r.publish(channel, message)
        return get_success_response({"success":True})
