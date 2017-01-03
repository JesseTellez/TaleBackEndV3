from app import db
from flask import current_app
import app.controllers.UserController as user_controller
from app.models.User import User as db_user
from flask_security import utils
from app.models.Story import Story as db_story
from app.utilities import RedisHandler as redis_handler

def login_user(email, password):
    app = current_app._get_current_object()
    if email is None or password is None:
        return False, "please provide email and password."
    user = db.session.query(db_user).filter(db_user.email == email).first()
    if user is None:
        return False, "user not found."
    if utils.verify_password(password, user.password_hash):
        token = user.generate_auth_token(app)
        return True, {'token': token.decode('ascii')}
    else:
        return False, "Invalide password."

def create_user(email, username, password):
    if email is None or username is None or password is None:
        return False, "Missing Data"

    new_user = db_user(
        email=email,
        username=username,
        password_hash=utils.encrypt_password(password)
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        results = {"user": new_user.serialize()}
        return True, results
    except:
        return False, "Error when saving to db."


def get_user(user_id):
    if user_id is None:
        return False, "user id not provided"
    user = db_user.query.filter_by(id=str(user_id)).first()
    if user is not None:
        results = {"user": user.serialize()}
        return True, results
    else:
        return False, "User not found"

def update_user(user_id, email, username, password, location, bio):
    if user_id is None:
        return False, "user id not provided"
    user = db_user.query.filter_by(id=str(user_id)).first()

    if user is None:
        return False, "user not found."

    if email is not None and len(email) > 0:
        user.email = email

    if username is not None and len(username) > 0:
        user.username = username

    if location is not None and len(location) > 0:
        user.city = location

    if bio is not None and len(bio) > 0:
        user.bio = bio

    if password is not None:
        user.password_hash = utils.encrypt_password(password)

    db.session.commit()
    result = {"user": user.serialize()}

    return True, result

def delete_user(user_id):
    if user_id is None:
        return False, "user id not provided."
    user = db_user.query.filter_by(id=str(user_id)).first()
    if user is None:
        return False, "user not found."
    db.session.delete(user)
    db.session.commit()
    return True, "user successfully deleted."



