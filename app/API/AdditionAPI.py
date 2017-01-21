from app import db
import app.controllers.AdditionController as addition_controller
from sqlalchemy import and_, exists
from app.models.Addition import Addition as db_addition
from app.models.Story import Story as db_story

from app.utilities.Publisher import Publisher
from app.utilities import RedisHandler as redis_handler

#This can probably be imported from the __init__
pub = Publisher()

def create_addition(story_id, owner_id, parent_id, content):
    #dont need to check for owner if we put an auth token on the user
    if content is not None and parent_id is not None and story_id is not None:
        story_exists = db.session.query(exists().where(db_story.id == story_id)).scalar()

        if story_exists is False:
            return False, "Story does not exist"
        story = db.session.query(db_story).get(story_id)
        parent = db.session.query(db_addition).filter(and_(db_addition.story_id == story_id, db_addition.id == parent_id)).first()
        if parent is not None:
            index_ref = addition_controller.calculate_index_ref(parent)
            new_addition = db_addition(
                content=str(content),
                owner_id=owner_id,
                story=story,
                parent_reference=parent,
                index_reference=index_ref,
                is_active=addition_controller.active_addition_exists_at_index_reference(story, index_ref)
            )
            db.session.add(new_addition)
            db.session.commit()
            addition_controller.save_addition_to_redis(story_id, new_addition)
            return True, {"message":"addition created"}
        else:
            return False, "story or parent does not exist"
    else:
        return False, "missing data"

def get_all_additions(story_id):
    if story_id is not None:
        story = db.session.query(db_story).get(story_id)
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
    return serializable_additions

def bookmark_addition(story_id, addition_id, user_id):
    story_exists = db.session.query(exists().where(db_story.id == story_id)).scalar()
    addition_exists = db.session.query(exists().where(db_addition.id == addition_id)).scalar()
    if story_exists is False:
        return False, "Story does not exist"
    if addition_exists is False:
        return False, "Addition does not exist"

    story = db.session.query(db_story).filter(db_story.id == story_id).first()
    addition = db.session.query(db_addition).filter(db_addition.id == addition_id).first()
    if addition.is_active:
        bookmark_success, count = addition_controller.redis_add_addition_bookmark(story_id, addition_id, user_id)
        if bookmark_success:
            message = "addition {additionid} now has {numlikes} bookmarks".format(additionid=addition_id, numlikes=count)
            return True, {"results": message}
        return False, "Unable to bookmark story"
    else:
        # Get LIKES for the ACTIVE ADDITION of this index for this story at this indexreference
        active_addition = next((aa for aa in story.additions if aa.index_reference == addition.index_reference and
                                aa.is_active is True), None)
        if active_addition is None:
            return False, "Something went wrong"

        bookmarks = redis_handler.get_bookmarks_for_addition(active_addition)

        bookmark_success, count = addition_controller.redis_add_addition_bookmark(story_id, addition_id, user_id)
        print count
        print "Bookmarks" + str(bookmarks)
        if count > bookmarks:
            print "am I getting here"
            addition_controller.change_active_addition(active_addition, addition)

        if bookmark_success:
            message = "addition {additionid} now has {numlikes} bookmarks".format(additionid=addition_id, numlikes=count)
            return True, {"results": message}
        return False, "Unable to bookmark story"
