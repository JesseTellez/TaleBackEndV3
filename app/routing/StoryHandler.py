from flask_restful import Resource
from app.routing import *
import app.API.StoryAPI as story_api

class StoryListHandler(Resource):
    """Handle Story creation"""
    @auth_required
    def post(self):
        req_json = request.get_json()
        if req_json is None:
            return get_error_response("Missing data, please fill out all fields")
        owner_id = req_json.get("owner_id", None)
        title = req_json.get("title", None)
        content = req_json.get("content", None)
        genre_id = req_json.get("genre_id", None)

        if owner_id is not None and title is not None and content is not None and genre_id is not None:
            success, message = story_api.create_story(
                owner_id=owner_id,
                title=title,
                content=content,
                genre_id=genre_id
            )
            return get_success_response(message) if success else get_error_response(message)
        else:
            return get_error_response("Some of the data is missing. Please fill out all of the required feilds")

    def get(self):
        """Get a list of all stories"""
        results = story_api.get_all_stories()
        if results is not None:
            return get_success_response(results)
            #return jsonify([story.serialize_for_feed() for story in all_stories])
        else:
            return get_error_response("No Stories Found.")

class StoryHandler(Resource):

    def get(self, story_id):
        """Get Story By ID"""
        try:
            story = story_api.get_story_by_id(story_id)
        except ValueError:
            return get_error_response("Could Not Find Story.")

        if story is not None:
            return get_success_response(story)
        else:
            return get_error_response("Must Provide A Story ID")

    @auth_required
    def post(self, story_id):
        """update existing story"""
        pass

    @auth_required
    def delete(self, story_id):
        """delete an existing story"""
        """NEED TO BE THE STORY OWNER"""
        pass

class StoryBookmarkHandler(Resource):
    """"""
    '''
    ---FORMAT---
    keys_values = [{
        key: 'story:{storyid}:likes',
        value: '{storyid}'
        tpye: "user_like"
    }]
    '''

    @auth_required
    def post(self, story_id):
        '''Bookmark(upvote) a story - this may track progress in the future'''
        '''SO the http request will send the data and then the python backend will publish to the client'''
        req_json = request.get_json()
        user_id = req_json["user_id"]
        success, message = story_api.bookmark_story(story_id, user_id)
        return get_success_response(message) if success else get_error_response(message)

