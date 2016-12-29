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

        if content is None or parent_id is None:
            return get_error_response("One or more params is missing, unable to create addition")

        # Have to make a check that the parent that is found points to a story with the same story id, otherwise the parent logic is off
        # story_information = db.session.query(Story).join(Story.additions).filter(and_(Addition.parent_id == parent_id, Story.id == story_id))
        story = Story.query.get_or_404(story_id)
        parent = db.session.query(Addition).filter(
            and_(Addition.story_id == story_id, Addition.id == parent_id)).first()
        if parent is not None:
            new_addition = Addition(
                content=content,
                owner_id=owner_id,
                story=story,
                parent_reference=parent,
                index_reference=generate_index_reference(parent)
            )
            db.session.add(new_addition)
            db.session.commit()
        else:
            return jsonify(msg="No Story was found for this addition, please try again."), 400
        return jsonify({"message": "addition successfully added to story"})
        # need to reevaluate active additions

    def get(self, story_id):
        """get all additions for story"""
        all_additions = db.session.query(Addition).filter(Addition.story_id == story_id).all()
        return [addition.to_json() for addition in all_additions]

class ActiveAdditionHandler(Resource):

    def get(self):
        # get all addition for ACTIVE addition - WORK IN PROGRESS
        req_json = request.get_json()
        story_id = req_json.get("owner_id", None)
        addition_id = req_json.get("parent_id", None)
        if story_id is None or addition_id is None:
            return jsonify(msg="One or more arguements is missing, please try again"), 400
        related_additions = db.session.query(Addition).filter(Addition.parent_id == addition_id).all()
        json_array = []
        for add in related_additions:
            json_array.append(default_parser(add))
        return jsonify(relatedAdditions=json_array)