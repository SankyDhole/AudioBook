from application import db
from flask_sqlalchemy import SQLAlchemy
from enum import Enum


class AudioTypes(Enum):
    song = 1
    podcast = 2
    Audiobook = 3


class SongInfo(db.Model):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    upload_time = db.Column(db.DateTime)


class podcastInfo(db.Model):
    __tablename__ = 'podcast_info'
    podcast_id = db.Column(db.Integer, primary_key=True)
    podcast_name = db.Column(db.String(100), nullable=False)
    podcast_duration = db.Column(db.Integer, nullable=False)
    podcast_upload_time = db.Column(db.DateTime)
    podcast_host = db.Column(db.String(100), nullable=False)
    podcast_participants = db.Column(db.JSON)


class AudiobookInfo(db.Model):
    __tablename__ = 'audiobook_info'
    audiobook_id = db.Column(db.Integer, primary_key=True)
    audiobook_title = db.Column(db.String(100), nullable=False)
    audiobook_author = db.Column(db.String(100), nullable=False)
    audiobook_upload_time = db.Column(db.DateTime)
    audiobook_narrator = db.Column(db.String(100), nullable=False)
    audiobook_duration = db.Column(db.Integer, nullable=False)


db.create_all()
db.session.commit()
