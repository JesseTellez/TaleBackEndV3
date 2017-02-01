from flask import json
from app import db
from sqlalchemy import exc, exists
from sqlalchemy.ext.declarative import DeclarativeMeta

from app.models.Premise import Premise as db_premise
from app.models.Character import Character as db_character
from app.models.Confilt import Conflict as db_conflict
from app.models.Timeline import Timelinse as db_timeline
#resolutions will go here
from app.models.User import User as db_user

from app.utilities import RedisHandler as redis_handler
from app.utilities.Publisher import Publisher
import app.controllers.PremiseController as Controller

def get_premise_by_id(premise_id):

    if premise_id is None:
        return None

    premise = db.session.query(db_premise).get(premise_id)

    if premise is None:
        return None

    serialized_conflicts = [conflict.serialize() for conflict in premise.conflicts.all()]
    serialized_timline = premise.timeline.serialize()
    serialized_characters = [character.serialize() for character in premise.characters.all()]

    results = premise.serialize(serialized_conflicts=serialized_conflicts, serialized_timeline=serialized_timline,
                                serialized_characters=serialized_characters)

    return results


def create_premise():

    pass

def promote_premise():
    pass