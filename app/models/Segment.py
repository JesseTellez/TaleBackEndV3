#this needs to have a floating property (let it swim)

#this can be any sort of segment for a story


from datetime import datetime
from app import db


class Segment(db.Model):

    __tablename__ = "story_segment"

    id = db.Column(db.Integer, primary_key=True)
    segment_type = db.Column(db.Integer, nullable=False)