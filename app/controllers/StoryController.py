from flask import Blueprint, request, g, jsonify, json
from .. import db
from flask_login import current_user
from sqlalchemy.sql import exists
from sqlalchemy import and_
import app.utilities as util
from app.models import Story, Addition, Vote
from sqlalchemy.ext.declarative import DeclarativeMeta
# define the blueprint: 'story' - set the url prefix to story
mod_story = Blueprint('story', __name__, url_prefix='/story')

@mod_story.route('/active_additions/', methods=['GET'])
def get_active_additions_for_story(storyid):
    '''WORK IN PROGRESS'''
    pass

@mod_story.route('/all', methods=['GET'])
def get_all_stories(serialize=True):
    all_stories = db.session.query(Story).order_by(Story.title).all()
    if serialize:
        return jsonify([story.to_feed_json() for story in all_stories])


@mod_story.route('/<int:storyid>/', methods=['GET'])
def get_story(storyid, serialize=True):
    story = get_story_helper(storyid)
    if serialize:
        return jsonify(story)

@mod_story.route('/<int:storyid>/', methods=['PUT'])
def update_story(options, serialize=True):
    story_to_update = db.session.query(Story).get(id)
    '''WORK IN PROGRESS'''


@mod_story.route('/', methods=['POST'])
def add_story():
    #need to do this for the application/json content type
    dataDict = json.loads(request.data)
    #find an owner with this
    owner_id = None
    if 'owner_id' in dataDict:
        owner_id = dataDict['owner_id']
    title = None
    if 'title' in dataDict:
        title = dataDict['title']
    content = None
    if 'content' in dataDict:
        content = dataDict['content']
    genre_id = None
    if 'genre_id' in dataDict:
        genre_id = dataDict['genre_id']

    if dataDict is None:
        return jsonify({"message": "Missing data, be sure to fill out all of the fields"})

    if owner_id is None or content is None or title is None or genre_id is None:
        return jsonify({"message": "Some of the data is missing. Please fill out all of the required feilds"})

    success = False
    new_story = Story(
        title=title,
        is_trending=False,
        unique_indicies=1,
        owner_id=owner_id,
        genre_id=genre_id
    )
    new_story_base = Addition(
        content=content,
        owner_id=owner_id,
        #notice I use the backref here (what I think is the backref)
        story=new_story
    )
    try:
        #only need to add this since we set up the relationship - dont mess with foriegn keys!!!
        db.session.add(new_story_base)
        db.session.commit()
        success = True
    except:
        db.session.rollback()

    if success is True:
        return jsonify({"message": "Story Successfully Created!"})
    else:
        return jsonify({"message": "Failed to create story.  Please try again."})


@mod_story.route('/<int:story_id>/bookmark', methods=['POST'])
def bookmark_story(story_id):
    current_user_id = 5
    bookmark_exists = db.session.query(
        exists().where(and_(Vote.StoryVote.user_id == current_user_id, Vote.StoryVote.story_id == story_id))).scalar()
    print("THIS IS BOOKMARK EXISTS STATUS" + str(bookmark_exists))
    if bookmark_exists:
        print("THE BOOKMARK EXISTS")
        db.session.query(Vote.StoryVote).filter(
            and_(Vote.StoryVote.user_id == current_user_id, Vote.StoryVote.story_id == story_id)).delete()
        db.session.commit()
    else:
        new_bookmark = Vote.StoryVote(
            user_id=current_user_id,
            story_id=story_id
        )
        db.session.add(new_bookmark)
        db.session.commit()
    return get_story_helper(story_id)


@mod_story.route('/<int:story_id>/new_addition', methods=['POST'])
def create_addition(story_id):
    dataDict = json.loads(request.data)

    '''Safety Checks'''
    if dataDict is None:
        return jsonify(msg="Missing Params"), 400
    content = None
    #story_id = request.args.get('story_id')
    if 'content' in dataDict:
        content = dataDict["content"]
    parent_id = None
    if 'parent_id' in dataDict:
        parent_id = dataDict["parent_id"]
    owner_id = None
    if 'owner_id' in dataDict:
        owner_id = dataDict["owner_id"]
    if content is None or parent_id is None:
        return jsonify(msg="One or more parameters from the request are missing."), 400

    #Have to make a check that the parent that is found points to a story with the same story id, otherwise the parent logic is off
    #story_information = db.session.query(Story).join(Story.additions).filter(and_(Addition.parent_id == parent_id, Story.id == story_id))
    story = Story.query.get_or_404(story_id)
    parent = db.session.query(Addition).filter(and_(Addition.story_id == story_id, Addition.id == parent_id)).first()
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


    return jsonify({"message":"addition successfully added to story"})
    # need to reevaluate active additions

@mod_story.route('/<int:story_id>/<int:addition_id>', methods=["GET"])
def get_all_additions_for_active_addition():
    #for the screen to see all active additions
    story_id = request.args.get('story_id')
    addition_id = request.args.get('addition_id')
    if story_id is None or addition_id is None:
        return jsonify(msg="One or more arguements is missing, please try again"), 400
    related_additions = db.session.query(Addition).filter(Addition.parent_id == addition_id).all()
    json_array = []
    for add in related_additions:
        json_array.append(default_parser(add))
    return jsonify(relatedAdditions=json_array)

@mod_story.route('/<int:story_id>/additions/<int:addition_id>', methods=['POST'])
def bookmark_addition(story_id, addition_id):
    current_user_id = 4  # we can possibly get this from the request params
    # I dont want to do all these queries EVERYTIME I get a like
    bookmark_exists = db.session.query(exists().where(Vote.AdditionVote.user_id == current_user_id)).scalar()
    if bookmark_exists:
        db.session.query(Vote.AdditionVote).filter(
            and_(Vote.AdditionVote.user_id == current_user_id, Vote.AdditionVote.addition_id == addition_id)).delete()
        db.session.commit()
    else:
        new_bookmark = Vote.AdditionVote(
            user_id=current_user_id,
            addition_id=addition_id
        )
        db.session.add(new_bookmark)
        db.session.commit()
    #MAKE IT SO THE STORY IS BASED ON GENRES, NOT CREATING STORIES AND THAT THE ADDITIONS ARE NOT VISABLE TO EACH OTHER?
    #the issue is I just want to update the story right then and there....not reload it all
    #just return the new value?
    #probably want to do a redis pub/sub for this or work with socket IO
    return get_story_helper(story_id)


@mod_story.route('/<int:story_id>/additions', methods=['GET'])
def get_all_additions_for_story(story_id):
    all_additions = db.session.query(Addition).filter(Addition.story_id == story_id).all()
    return [addition.to_json() for addition in all_additions]

@mod_story.route('/testing', methods=['GET'])
def make_testing_variables():
    pass

def get_story_helper(story_id):
    print("THIS IS MY STORY ID " + str(story_id))
    storyQuery = db.session.query(Story).get(story_id)
    base = None
    # update this to get the active additions
    serialized_addtions = []
    for addition in storyQuery.additions.all():
        if addition.index_reference is None:
            base = addition
        else:
            serialized_addtions.append(default_parser(addition))
    print("IM GETTING HERE!!!!!!!!!!")
    return {"story": storyQuery.to_json(base.to_json(), serialized_addtions)}

def generate_index_reference(parent):
    if parent is not None:
        return 0 if parent.index_reference is None else parent.index_reference + 1
    else:
        return None


def default_parser(o):
    if isinstance(o, tuple):
        data = {}
        for obj in o:
            data.update(parse_sqlalchemy_object(obj))
        return data
    if isinstance(o.__class__, DeclarativeMeta):
        return parse_sqlalchemy_object(o)
    return json.JSONEncoder.default(o)


def parse_sqlalchemy_object(o):
    data = {}
    fields = o.to_json() if hasattr(o, 'to_json') else dir(o)
    for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
        value = o.__getattribute__(field)
        try:
            json.dumps(value)
            data[field] = value
        except TypeError:
            data[field] = None
    return data
