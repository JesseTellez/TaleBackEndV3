from app import db
from sqlalchemy import and_, exists, or_, in_
from app.models.Character import Character as db_character
from app.model.Trait import Trait as db_trait
from app.model.User import User as db_user

from app.utilities.Publisher import Publisher
from app.utilities import RedisHandler as redis_handler


def create_character(name, description, age, trait_ids, owner_id, premise_id=None, conflict_id=None, time_line_id=None):
    #ONCE CREATED - DO BACKGROUND WORK AND NOTIFY/ADD TO THE RECOMMENDED LISTS THAT APPLY FOR THIS ITEM

    #is this a character to an existing segment?

    #conflict
    if conflict_id is not None:
        create_character_for_conflict()

    #premise
    if premise_id is not None:
        create_character_for_premise()

    #timeline
    if time_line_id is not None:
        create_character_for_timeline()

    if premise_id is None and conflict_id is None and time_line_id is None:
        #this is a new character from scratch

        owner = db.session.query(db_user).filter(db_user.id == owner_id).first()

        #grab the traints within my list and catagirize them
        all_traits = db.session.query(db_trait).filter(db_trait.id.in_(trait_ids)).all()
        #TODO - make association tables for these (many to many)
        personality_traits = [trait for trait in all_traits if trait.type == 1]

        motivation_traits = [trait for trait in all_traits if trait.type == 2]

        new_character = db_character(
            name=name,
            image="",
            description=description,
            age=age,
            owner=owner
        )
        for trait in all_traits:
            #I need to add to this other side too
            new_character.personal_traits.append(trait)

        try:
            db.session.add(new_character)
            db.session.commit()
        except:
            print("Something went wrong when adding a character")



def get_character_by_id(character_id):

    character = db.session.query(db_character).filter(db_character.id == character_id).first()

    json_traits = [trait.serialize() for trait in character.personal_traits]

    json_premises = []

    json_timelines = []

    json_character = character.serialize(serialized_personal_traits=json_traits, serialized_premises=json_premises,
                                         serialized_owner=character.owner.serialize())

    return True, json_character




def create_character_for_conflict():
    #find the motive_traits associated with this conflict and add them to the character
    pass

def create_character_for_premise():
    #figure out how this character fits this premise
    pass

def create_character_for_timeline():
    #figure out how this character fits this timeline
    pass