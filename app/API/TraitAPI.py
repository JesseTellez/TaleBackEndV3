from app import db
from sqlalchemy import and_, exists, or_
from app.models.Character import Character as db_character
from app.models.Trait import Trait as db_trait
from app.models.User import User as db_user

from app.utilities.Publisher import Publisher
from app.utilities import RedisHandler as redis_handler



def create_trait(title, description, wisdom_level,
                 courage_level, humanity_level, justice_level, temperance_level, trancendance_level):

    new_trait = db_trait(
        title=title,
        description=description,
        wisdom_level=wisdom_level,
        courage_level=courage_level,
        humanity_level=humanity_level,
        justice_level=justice_level,
        temperance_level=temperance_level,
        trancendance_level=trancendance_level
    )

    db.session.add(new_trait)
    db.session.commit()

    return True, "Successfully created trait"


def get_trait(trait_id):

    trait = db.session.query(db_trait).get(trait_id)
    return True, trait.serialize()


def get_all_traits():
    traits = db.session.query(db_trait).all()
    serialized_traits = [trait.serialize() for trait in traits]

    return {"traits": serialized_traits}

def create_test_traits():
    '''For Testing purposes only'''

    #sliding the values should affect the others (done in app)
    test_trait_1 = db_trait(
        title="Determined",
        description="Characters that are determined for-go on their path without consideration of hindering factors",
        wisdom_level=30,
        courage_level=95,
        humanity_level=20,
        justice_level=10,
        temperance_level=45,
        trancendance_level=10
    )

    test_trait_2 = db_trait(
        title="Mindful",
        description="This trait defines characters ",
        wisdom_level=80,
        courage_level=35,
        humanity_level=90,
        justice_level=90,
        temperance_level=75,
        trancendance_level=50
    )

    test_trait_3 = db_trait(
        title="Loving",
        description="Cares for everyone and establishes realationships on a personal level",
        wisdom_level=40,
        courage_level=20,
        humanity_level=100,
        justice_level=60,
        temperance_level=70,
        trancendance_level=90
    )

    test_trait_4 = db_trait(
        title="Ho-Ready",
        description="This dude ho-ready",
        wisdom_level=100,
        courage_level=100,
        humanity_level=100,
        justice_level=100,
        temperance_level=100,
        trancendance_level=100
    )
    test_trait_list = [test_trait_1, test_trait_2, test_trait_3, test_trait_4]

    for trait in test_trait_list:
        db.session.add(trait)
    db.session.commit()