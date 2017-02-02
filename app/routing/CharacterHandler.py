from flask_restful import Resource
from app.routing import *
import app.API.CharacterAPI as character_api


class CharacterListHandler(Resource):

    def post(self):
        '''create a new character'''

        req_json = request.get_json()

        if req_json is None:
            return get_error_response("Missing data, please fill out all fields")

        trait_ids = [1,2,3]

        name = req_json.get("name", None)

        description = req_json.get("description", None)

        age = req_json.get("age", None)

        owner_id = req_json.get("owner_id", None)

        success, results = character_api.create_character(name=name,
                                                          description=description,
                                                          age=age,
                                                          trait_ids=trait_ids,
                                                          owner_id=owner_id
                                                          )

        return get_success_response(results) if success else get_error_response(results)


class TestCharacterHandler(Resource):

    def get(self):
        character_api.create_test_characters()
