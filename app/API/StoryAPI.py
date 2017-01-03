from flask import json
from app import db
from sqlalchemy import exc
from app.models.Addition import Addition as db_addition
from app.models.Story import Story as db_story
from app.utilities import RedisHandler as redis_handler
from sqlalchemy.ext.declarative import DeclarativeMeta
from app.utilities.Publisher import Publisher

pub = Publisher()


def get_story_by_id(story_id):

    if story_id is not None:
        story = db.session.query(db_story).get(story_id)
        if story is not None:
            base = None
            # update this to get active additions
            serialized_additions = []
            for addition in story.additions.all():
                if addition.index_reference is None:
                    base = addition
                else:
                    serialized_additions.append(default_parser(addition))
            results = {"story": story.serialize(
                base=base.to_json(),
                adds=serialized_additions,
                #THIS NEEDS TO BE UPDATED
                unique_indicies=None
            )}
            return results
        else:
            raise ValueError('Unable to find story')
    else:
        return None

def create_story(owner_id, title, content, genre_id):

    if owner_id is not None and title is not None and content is not None and genre_id is not None:
        new_story = db_story(
            title=str(title),
            is_trending=False,
            unique_indicies=1,
            owner_id=owner_id,
            genre_id=genre_id
        )

        new_story_base = db_addition(
            content=str(content),
            owner_id=owner_id,
            story=new_story
        )

        try:
            db.session.add(new_story_base)
            db.session.commit()
            return True
        except exc.NoReferencedTableError:
            db.session.rollback()
            return False
    else:
        return False

def update_story(story_id):
    pass

def get_all_stories():
    all_stories = db.session.query(db_story).order_by(db_story.title).all()
    return all_stories

def bookmark_story(story_id, user_id):
    redis_story_set = 'story:{storyid}:likes'.format(storyid=story_id)
    redis_story_set_dict = {
        "key": redis_story_set,
        "value": user_id,
        "type": "user_like"
    }
    success, count = redis_handler.save_to_redis(redis_story_set_dict)

    redis_user_set = 'user:{userid}:likes'.format(userid=user_id)
    redis_user_set_dict = {
        "key": redis_user_set,
        "value": story_id,
        "type": "story_like"
    }
    redis_handler.save_to_redis(redis_user_set_dict)

    pub.channel = 'LikeChannel'

    dict = {
        "story_id": story_id,
        "likes": count
    }

    redis_success = False
    if success:
        redis_success = pub.create_and_send_message(dict)

    if redis_success:
        return True
    else:
        return False

def default_parser(o):
    if isinstance(o, tuple):
        data = {}
        for obj in o:
            data.update(parse_sqlalchemy_object(obj))
        return data
    if isinstance(o.__class__, DeclarativeMeta):
        return parse_sqlalchemy_object(o)
    return json.JSONEncoder.default(o)


def parse_sqlalchemy_object(o):
    data = {}
    fields = o.to_json() if hasattr(o, 'to_json') else dir(o)
    for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
        value = o.__getattribute__(field)
        try:
            json.dumps(value)
            data[field] = value
        except TypeError:
            data[field] = None
    return data
