import os
from datetime import datetime
from flask_restful import Resource
from app.models.User import User as db_user
from app import db
from app.routing import *
from werkzeug.utils import secure_filename

from app.utilities import RedisHandler as redis_handler
from app.utilities.Publisher import Publisher

import app.API.UserAPI as user_api

class LoginHandler(Resource):
    """Class to handle user login route"""
    def post(self):
        """Log User In"""
        req_json = request.get_json()
        email = req_json["email"]
        password = req_json["password"]
        success, results = user_api.login_user(email, password)
        return get_success_response(results) if success else get_error_response(results)


class ProfilePic(Resource):
    """Class to Handle profile pic routes"""
    @auth_required
    def post(self, user_id):
        """Update profile picture"""
        app = current_app._get_current_object()

        file = request.files['file-0']
        if file:
            #Save the pic to the filesystem
            filename = secure_filename(user_id + "_" + datetime.now().strftime("%Y%m%d%H%M%S"))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            user = db_user.query.filter_by(id=str(user_id)).first()

            #Delete the old pic if there is one
            if user.profile_pic_url is not None:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.profile_pic_url))

                user.profile_pic_url = filename
                db.session.commit()
                result = { "filename": filename }
                return get_success_response(result)
        return get_error_response("Upload Error")

class UserListHandler(Resource):
    """class to handle user creation routes"""
    def post(self):
        """Create new user"""
        req_json = request.get_json()
        email = req_json.get("email", None)
        username = req_json.get("username", None)
        password = req_json.get('password', None)
        success, message = user_api.create_user(email, username, password)
        return get_success_response(message) if success else get_error_response(message)

class UserHandler(Resource):
    """Class for handling fetching, updating, and deleting users"""
    @auth_required
    def get(self, user_id):
        """Fetch user"""
        success, message = user_api.get_user(user_id)
        return get_success_response(message) if success else get_error_response(message)

    @auth_required
    def post(self, user_id):
        """Update User"""
        req_json = request.get_json()
        email = req_json.get('email', None)
        username = req_json.get('username', None)
        password = req_json.get('password', None)
        location = req_json.get('location', None)
        bio = req_json.get('bio', None)
        user = db_user.query.filter_by(id=str(user_id)).first()
        if user is not None:
            # if req.body was provided then there is nothing to update
            if len(req_json) <= 0:
                result = {"user": user.serialize}
                return get_success_response(result)
            success, message = user_api.update_user(user_id, email, username, password, location, bio)
            return get_success_response(message) if success else get_error_response(message)
        else:
            return get_error_response("user not found")

    def delete(self, user_id):
        """Delete User"""
        success, message = user_api.delete_user(user_id)
        return get_success_response(message) if success else get_error_response(message)