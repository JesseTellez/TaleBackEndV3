import flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_restful import Resource, Api
from flask_security import Security, SQLAlchemyUserDatastore
import pymysql

import redis

config2 = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

r = redis.StrictRedis(**config2)
#need this to load the mysqldb module in the app
pymysql.install_as_MySQLdb()

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object(config['development'])
    config['development'].init_app(app)
    app.config["SECRET_KEY"] = "SunshineSucks"

    db.init_app(app)
    login_manager.init_app(app)

    api = Api(app)

    from .controllers.StoryController import mod_story as story_blueprint
    app.register_blueprint(story_blueprint)

    from controllers.UserController import Login, UserList, UserStoryLike
    from app.models import User as db_user, Role


    user_datastore = SQLAlchemyUserDatastore(db, db_user, Role)
    security = Security()
    security.init_app(app, user_datastore)

    api.add_resource(Login, '/user/login')
    api.add_resource(UserList, '/users')
    api.add_resource(UserStoryLike, '/story/likes')

    return app


def upvote_subscriber():
    # this should always be running!!!!
    channel = 'LikeChannel'
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    '''
    key = 'story:{storyid}:likes'.format(storyid=story_id)
    value = '{userid}'.format(userid=user_id)
    r.sadd(key, value)
    key2 = 'user:{userid}:likes'.format(userid=user_id)
    value2 = '{storyid}'.format(story_id)
    r.sadd(key2, value2, key)
    '''
    while True:
        for item in pubsub.listen():
            print item['data']