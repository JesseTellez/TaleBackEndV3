from flask_restful import Resource
from app.routing import *
import app.API.AdditionAPI as addition_api

class AdditionListHandler(Resource):

    #@mod_story.route('/<int:story_id>/new_addition', methods=['POST'])
    def post(self, story_id):
        """create a new addition for story"""
        req_json = request.get_json()
        if req_json is None:
            return get_error_response("Missing data, unable to create addition")
        owner_id = req_json.get("owner_id", None)
        parent_id = req_json.get("parent_id", None)
        content = req_json.get("content", None)

        success = addition_api.create_addition(story_id, owner_id, parent_id, content)
        return get_success_response({"message": "addition succesfully created"}) if success else get_error_response("failed to create addition")

    def get(self, story_id):
        """get all additions for story"""
        try:
            results = addition_api.get_all_additions(story_id)
            return get_success_response(results)
        except ValueError:
            return get_error_response("something went wrong")


class ActiveAdditionHandler(Resource):

    def get(self):
        # get all additions for ACTIVE addition - WORK IN PROGRESS
        req_json = request.get_json()
        story_id = req_json.get("owner_id", None)
        addition_id = req_json.get("parent_id", None)
        try:
            additions = addition_api.get_additions_for_active_addition(story_id, addition_id)
            return get_success_response(additions)
        except ValueError:
            return get_error_response("something went wrong when grabbing additions for active")