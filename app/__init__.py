import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore
import pymysql
import redis

config2 = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config2)
pymysql.install_as_MySQLdb()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app():

    app = flask.Flask(__name__)
    app.config.from_object(config['development'])
    config['development'].init_app(app)
    app.config["SECRET_KEY"] = "SunshineSucks"
    app.config['SECURITY_REGISTERABLE'] = True
    app.config["SECURITY_CONFIRMABLE"] = False
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False
    app.config["SECURITY_PASSWORD_HASH"] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = 'xxxxxxxxxxxx'
    app.config['SECRET_KEY'] = 'FmG9yqMxVfb9aoEVpn6J'

    db.init_app(app)
    login_manager.init_app(app)

    api = Api(app)

    from app.routing.StoryHandler import StoryListHandler, StoryHandler, StoryBookmarkHandler, TestStoryHandler
    from app.routing.AdditionHandler import AdditionListHandler, ActiveAdditionHandler, AdditionBookmarkHandler
    from app.routing.UserHandler import LoginHandler, UserListHandler, UserHandler, TestUserHandler
    from app.routing.CharacterHandler import TestCharacterHandler, CharacterListHandler
    from app.routing.TraitHandler import TestTraitHandler
    from app.models import User as db_user, Role


    user_datastore = SQLAlchemyUserDatastore(db, db_user, Role)
    security = Security()
    security.init_app(app, user_datastore)

    #USERS
    api.add_resource(LoginHandler, '/user/login')
    api.add_resource(UserListHandler, '/users')
    api.add_resource(UserHandler, '/user/<user_id>')

    #BASE STORIES
    api.add_resource(StoryBookmarkHandler, '/story/<story_id>/likes')
    api.add_resource(StoryListHandler, '/stories')
    api.add_resource(StoryHandler, '/story/<story_id>')

    #BASE EXTENSIONS
    api.add_resource(AdditionListHandler, '/<story_id>/additions')
    api.add_resource(AdditionBookmarkHandler, '/story/<story_id>/additions/<addition_id>/bookmarks')

    #STORY CREATOR CHARACTERS
    api.add_resource(CharacterListHandler, '/characters')


    #Test Routes
    api.add_resource(TestCharacterHandler, '/test/characters')
    api.add_resource(TestTraitHandler, '/test/traits')
    api.add_resource(TestStoryHandler, '/test/stories')
    api.add_resource(TestUserHandler, '/test/users')


    return app

