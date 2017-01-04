from flask_restful import Resource
from app.routing import *
import app.API.AdditionAPI as addition_api

class AdditionListHandler(Resource):

    def post(self, story_id):
        """create a new addition for story"""
        req_json = request.get_json()
        if req_json is None:
            return get_error_response("Missing data, unable to create addition")
        owner_id = req_json.get("owner_id", None)
        parent_id = req_json.get("parent_id", None)
        content = req_json.get("content", None)

        success, message = addition_api.create_addition(story_id, owner_id, parent_id, content)
        return get_success_response(message) if success else get_error_response(message)

    def get(self, story_id):
        """get all additions for story"""
        try:
            results = addition_api.get_all_additions(story_id)
            return get_success_response(results)
        except ValueError, e:
            return get_error_response(e.message)

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


class AdditionBookmarkHandler(Resource):
    """"""
    '''
    ---FORMAT---
    keys_values = [{
        key: 'story:{storyid}:likes',
        value: '{storyid}'
        tpye: "user_like"
    }]
    '''
    def post(self, story_id, addition_id):
        '''Bookmark(upvote) a story - this may track progress in the future'''
        '''SO the http request will send the data and then the python backend will publish to the client'''
        '''IF THE UPVOTE TRIGGERS AN ADDITION SWITCH, I NEED TO PRODUCE THAT EVENT'''
        req_json = request.get_json()
        user_id = req_json["user_id"]
        success, message = addition_api.bookmark_addition(story_id, addition_id, user_id)
        return get_success_response(message) if success else get_error_response(message)


class ActiveAdditionListHandler(Resource):

    def get(self, story_id):
        """Get all active additions for story"""
