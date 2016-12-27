import json
from flask_restful import Resource
from ..models.User import User as db_user
from .. import db
from sqlalchemy.exc import IntegrityError
from app.controllers import *
from flask_security import utils
from app.utilities import RedisHandler as rHandle
from app.utilities.Publisher import Publisher

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
            # if req.body was provided then there is nothing to update
            if len(req_json) <= 0:
                result = {"user": user.serialize}
                return get_success_response(result)

            email = req_json.get('email', None)
            if email is not None and len(email) > 0:
                user.email = email

            username = req_json.get('username', None)
            if username is not None and len(username) > 0:
                user.username = username

            city = req_json.get('city', None)
            if city is not None and len(city) > 0:
                user.city = city

            bio = req_json.get('bio', None)
            if bio is not None and len(bio) > 0:
                user.bio = bio
            #check if user is changing their password
            password = req_json.get('password', None)
            confirm = req_json.get('confirm', None)
            if password is not None and confirm is not None:
                if password != confirm:
                    msg = "Password and confirmation do not match!"
                    return get_error_response(msg)
                else:
                    user.password_hash = utils.encrypt_password(password)

            db.session.commit()
            result = {"user": user.serialize}
            return get_success_response(result)
        else:
            return get_error_response("User does not exist!")

    def delete(self, user_id):
        """Delete User"""
        user = db_user.query.filter_by(id=str(user_id)).first()
        if user is None:
            return get_error_response("User not found.")
        db.session.delete(user)
        db.session.commit()
        return get_success_response()

class UserStoryLike(Resource):
    """Class for handling Upvotes to Stories"""

    '''
    ---FORMAT---
    keys_values = [{
        key: 'story:{storyid}:likes',
        value: '{storyid}'
        tpye: "user_like"
    }]
    '''
    pub = Publisher()

    def post(self):
        """upvote a story"""
        '''SO the http request will send the data and then the python backend will publish to the client'''
        req_json = request.get_json()
        story_id = req_json["story_id"]
        user_id = req_json["user_id"]

        redis_story_set = 'story:{storyid}:likes'.format(storyid=story_id)
        redis_story_set_dict = {
            "key": redis_story_set,
            "value": user_id,
            "type": "user_like"
        }
        success, count = rHandle.save_to_redis(redis_story_set_dict)

        redis_user_set = 'user:{userid}:likes'.format(userid=user_id)
        redis_user_set_dict = {
            "key": redis_user_set,
            "value": story_id,
            "type": "story_like"
        }
        rHandle.save_to_redis(redis_user_set_dict)

        self.pub.channel = 'LikeChannel'

        dict = {
            "story_id": story_id,
            "likes": count
        }

        print success
        print count

        redis_success = False

        if success:
            redis_success = self.pub.create_and_send_message(dict)

        if redis_success:
            return get_success_response({"results": True})
        else:
            return get_error_response("Server Error")


