from flask_restful import Resource
from app.routing import *
import app.API.StoryAPI as story_api

class StoryListHandler(Resource):
    """Handle Story creation"""
    def post(self):
        req_json = request.get_json()
        if req_json is None:
            return get_error_response("Missing data, please fill out all fields")
        owner_id = req_json.get("owner_id", None)
        title = req_json.get("title", None)
        content = req_json.get("content", None)
        genre_id = req_json.get("genre_id", None)
        #current_user = db_user.query.filter_by(id=owner_id).first()

        if owner_id is not None and title is not None and content is not None and genre_id is not None:
            success = story_api.create_story(
                owner_id=owner_id,
                title=title,
                content=content,
                genre_id=genre_id
            )
            if success is True:
                return jsonify({"message": "Story Successfully Created!"})
            else:
                return jsonify({"message": "Failed to create story.  Please try again."})
        else:
            return get_error_response("Some of the data is missing. Please fill out all of the required feilds")

    def get(self):
        """Get a list of all stories"""
        all_stories = story_api.get_all_stories()
        if all_stories is not None:
            results = [story.serialize_for_feed() for story in all_stories]
            return get_success_response(results)
            #return jsonify([story.serialize_for_feed() for story in all_stories])
        else:
            return get_error_response("No Stories Found.")

class Story(Resource):

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

    def post(self, story_id):
        """update existing story"""
        pass

    def delete(self, story_id):
        """delete an existing story"""
        pass

