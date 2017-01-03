from app import db
import app.controllers.AdditionController as addition_controller
from sqlalchemy import and_
from app.models.Addition import Addition as db_addition
from app.models.Story import Story as db_story
from app.utilities import RedisHandler as redis_handler

def create_addition(story_id, owner_id, parent_id, content):
    #dont need to check for owner if we put an auth token on the user
    if content is not None and parent_id is not None and story_id is not None:
        # Have to make a check that the parent that is found points to a story with the same
        # story id, otherwise the parent logic is off
        # story_information = db.session.query(Story).join(Story.additions).filter(and_(Addition.parent_id == parent_id, Story.id == story_id))
        story = db.session.query(db_story).get(story_id)
        parent = db.session.query(db_addition).filter(and_(db_addition.story_id == story_id, db_addition.id == parent_id)).first()
        if story is not None and parent is not None:
            new_addition = db_addition(
                content=str(content),
                owner_id=owner_id,
                story=story,
                parent_reference=parent,
                index_referenec=addition_controller.calculate_index_ref(parent)
            )
            db.session.add(new_addition)
            db.session.commit()
            return True
        else:
            return False
    else:
        return False

def get_all_additions(story_id):
    if story_id is not None:
        story = db_addition.session.query(db_story).get(story_id)
        if story is not None:
            all_additions = db.session.query(db_addition).filter(db_addition.story_id == story_id).all()
            results = {"additions": [addition.serialize_for_list() for addition in all_additions]}
            return results
        else:
            raise ValueError("story does not exist")
    else:
        raise ValueError("no story id provided")

def get_additions_for_active_addition(story_id, addition_id):
    if story_id is None or addition_id is None:
        raise ValueError("no story id or addition id provided")
    story = db.session.query(db_story).get(story_id)
    addition = db.session.query(db_addition).get(addition_id)
    #Might not even need this if block if an empty query returns a exception
    if story is None or addition is None:
        raise ValueError("could not find story or addition")
    related_additions = db.session.query(db_addition).filter(db_addition.parent_id == addition_id).all()
    '''Grab bookmarks for addition'''
    serializable_additions = []
    for addition in related_additions:
        id = addition.id
        redis_addition_set = 'story:{additionid}:likes'.format(additionid=id)
        #make sure this returns 0 of no addition is found
        bookmarks = redis_handler.get_set_count(redis_addition_set)
        json_addition = addition.serialize(bookmarks)
        serializable_additions.append(json_addition)
    #might need to use the parser here
    # for add in related_additions:
    #     json_array.append(default_parser(add))
    # return jsonify(relatedAdditions=json_array)
    return serializable_additions
