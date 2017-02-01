from flask_restful import Resource
from app.routing import *
import app.API.TraitAPI as trait_api


class TraitListHandler(Resource):

    #Create a new trait
    def post(self):

        req_json = request.get_json()

        if req_json is None:
            return get_error_response("Missing data error.")

        title = req_json.get("title", None)
        description = req_json.get("description", None)
        wisdom = req_json.get("wisdom", None)
        courage = req_json.get("courage", None)
        humanity = req_json.get("humanity", None)
        justice = req_json.get("justice", None)
        temperance = req_json.get("temperance", None)
        trancendance = req_json.get("trancendance", None)

        success, results = trait_api.create_trait(title=title,
                                                  description=description,
                                                  wisdom_level=wisdom,
                                                  courage_level=courage,
                                                  humanity_level=humanity,
                                                  justice_level=justice,
                                                  temperance_level=temperance,
                                                  trancendance_level=trancendance
                                                  )

        return get_success_response(results) if success else get_error_response(results)


    def get(self):
        '''get all triats in db'''

        all_triats = trait_api.get_all_traits()

        return get_success_response(all_triats)


class TestTraitHandler(Resource):

    def get(self):
        trait_api.create_test_traits()