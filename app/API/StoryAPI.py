from flask import request, g, jsonify, json
from app import db
from sqlalchemy.sql import exists
from sqlalchemy import and_, exc
from app.models.Addition import Addition as db_addition
from app.models.Story import Story as db_story
from app.models.User import User as db_user
from sqlalchemy.ext.declarative import DeclarativeMeta

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
