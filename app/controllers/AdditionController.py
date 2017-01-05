from app import r
import json

def calculate_index_ref(addition):
    if addition.index_reference is not None:
        return addition.index_reference + 1
    return 0

def generate_index_reference(parent):
    if parent is not None:
        return 0 if parent.index_reference is None else parent.index_reference + 1
    else:
        return None


def change_active_addition():
    '''Publisher for the change event of an active addition'''
    '''the UI will be the subscriber and update the story real-time'''
    pass

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
    redis_key = 'story:{storyid}:additions'.format(storyid=story_id)
    addition_dict = {str(addition.id): 0}
    r.hset(redis_key, addition.id, 0)
