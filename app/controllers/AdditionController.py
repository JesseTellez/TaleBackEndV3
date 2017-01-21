from app import r, db
from app.models.Addition import Addition as db_addition
from app.models.Story import Story as db_story

from app.utilities import RedisHandler as redis_handler
from app.utilities.Publisher import Publisher
pub = Publisher()

def calculate_index_ref(addition):
    if addition.index_reference is not None:
        return addition.index_reference + 1
    return 0

def generate_index_reference(parent):
    if parent is not None:
        return 0 if parent.index_reference is None else parent.index_reference + 1
    else:
        return None

def change_active_addition(active_addition_old, active_addition_new):
    '''Publisher for the change event of an active addition'''
    '''the UI will be the subscriber and update the story real-time'''
    #Publish this event
    update_old_addition = db.session.update(db_addition).where(db_addition.id == active_addition_old.id).values(is_active=False)
    update_new_addition = db.session.update(db_addition).where(db_addition.id == active_addition_new.id).values(is_active=True)
    db.session.commit()
    pub.story_changed_event(active_addition_new.story_id, active_addition_new.index_reference)

def get_additions_at_index_reference(story, indexref):
    additions_at_index_reference = []
    for add in story.additions:
        if add.index_reference == indexref:
            additions_at_index_reference.append(add)
    return additions_at_index_reference


def initialize_redis_store():
    """use this to load addition data into the cache"""
    """load active additions and their bookmarks for each story hset"""
    # { active_addtion_1: 323 }
    pass

def save_addition_to_redis(story_id, addition):
    redis_key = 'story:{storyid}:bookmarks:additions'.format(storyid=story_id)
    r.hset(redis_key, addition.id, 0)

def get_active_additions_for_story(story):
    active_additions = []
    if story is None:
        return active_additions
    for add in story.additions:
        if add.is_active is True:
            active_additions.append(add)

    return active_additions

def active_addition_exists_at_index_reference(story, index_reference):
    if story is None:
        return False
    all_active_additions_for_story = [add for add in story.additions if add.is_active is True]
    addition = next((add for add in all_active_additions_for_story if add.index_reference == index_reference), None)
    return True if addition is None else False

def redis_add_addition_bookmark(story_id, addition_id, user_id):
    redis_addition_set = 'story:{storyid}:additions:{additionid}:bookmarks'.format(storyid=story_id,
                                                                                   additionid=addition_id)
    redis_addition_set_dict = {
        "key": redis_addition_set,
        "value": user_id,
        "type": "user_like"
    }
    success, count = redis_handler.save_to_redis(redis_addition_set_dict)

    pub.channel = 'LikeChannel'

    dict = {
        "addition": addition_id,
        "likes": count
    }
    if success:
        redis_success = pub.create_and_send_message(dict)
        if redis_success:
            return True, count

    return False, None