from flask import request, g, jsonify, json
from app import db
from sqlalchemy.sql import exists
from sqlalchemy import and_, exc
from app.models.Addition import Addition as db_addition
from app.models.Story import Story as db_story
from app.models.User import User as db_user
from sqlalchemy.ext.declarative import DeclarativeMeta


def create_addition(story_id):
    pass