from flask import Flask, request, jsonify, send_file
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
#from Models.model import *
from datetime import datetime
#from application import db
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

now = datetime.now()

application = app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sanket:apple@123@localhost:3305/db'
db = SQLAlchemy(app)


class AudioTypes(Enum):
    song = 1
    podcast = 2
    audiobook = 3


class SongInfo(db.Model):
    __tablename__ = 'song_info'
    song_id = db.Column(db.Integer, primary_key=True)
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

#TODO:
def get_songlist(listobject):
    song_list = []
    for i in listobject:
        getsong_dict = {}
        print (i.name)
        print (i.song_id)
        getsong_dict['name'] = i.name
        getsong_dict['song_id'] = i.song_id
        getsong_url = "127.0.0.1:5000/song/" + str(i.song_id)
        song_list.append(getsong_url)
    print (song_list)
    return song_list


def get_podlist(listobject):
    podcast_list = []
    for i in listobject:
        getpod_dict = {}
        getpod_dict['podcast_name'] = i.podcast_name
        getpod_dict['podcast_id'] = i.podcast_id
        getpod_url = "127.0.0.1:5000/podcast/" + str(i.podcast_id)
        podcast_list.append(getpod_url)
    print (podcast_list)
    return podcast_list

def get_audiolist(listobject):
    audio_list = []
    for i in listobject:
        getaudio_dict = {}
        getaudio_dict['audiobook_title'] = i.audiobook_title
        getaudio_dict['audiobook_id'] = i.audiobook_id
        getaudio_url = "127.0.0.1:5000/audiobook/" + str(i.audiobook_id)
        audio_list.append(getaudio_url)
    print (audio_list)
    return audio_list


@app.route('/<user>', methods=['POST'])
def create_user(user):
    try:
        receive_data = request.get_json()
        if user == AudioTypes(1).name:
            print("In song")
            songIn = SongInfo.query.filter_by(song_id=receive_data['song_id']).first()
            if songIn:
                response = {"status": "Failure", "msg": "Song already exist"}
                return jsonify(response)
            else:
                add_data = SongInfo(song_id=receive_data['song_id'], name=receive_data['name'],
                                    duration=receive_data['duration'], upload_time=datetime.now())
        if user == AudioTypes(2).name:
            podcastIn = podcastInfo.query.filter_by(podcast_id=receive_data['podcast_id']).first()
            if podcastIn:
                response = {"status": "Failure", "msg": "podcast already exist"}
                return jsonify(response)
            else:
                if len(receive_data['podcast_participants']) < 11 :
                    add_data = podcastInfo(podcast_id=receive_data['podcast_id'], podcast_name=receive_data['podcast_name'],
                                           podcast_duration=receive_data['podcast_duration'], podcast_upload_time=datetime.now(),
                                           podcast_host=receive_data['podcast_host'],
                                           podcast_participants=receive_data['podcast_participants'])
                else:
                    return "Failure", 400
        if user == AudioTypes(3).name:
            audiobookIn = AudiobookInfo.query.filter_by(audiobook_id=receive_data['audiobook_id']).first()
            if audiobookIn:
                response = {"status": "Failure", "msg": "podcast already exist"}
                return jsonify(response)
            else:
                add_data = AudiobookInfo(audiobook_id=receive_data['audiobook_id'],
                                         audiobook_title=receive_data['audiobook_title'],
                                         audiobook_author=receive_data['audiobook_author'],
                                         audiobook_duration=receive_data['audiobook_duration'],
                                         audiobook_upload_time=datetime.now(),
                                         audiobook_narrator=receive_data['audiobook_narrator'])

        db.session.add(add_data)
        db.session.commit()

    except Exception as exe:
        print(exe)
        return "Failure", 400
    return "Success", 200


@app.route('/<user>/<int:id>', methods=['PUT'])
def update_user(user, id):
    try:
        receive_update = request.get_json()
        print(receive_update)
        if user == AudioTypes(1).name:
            print("update")
            songupdate = SongInfo.query.filter_by(song_id=id).first()
            if not songupdate:
                response = {"status": "Failure"}
                return jsonify(response)
            else:
                songupdate.name = receive_update['name']
                songupdate.duration = receive_update['duration']
                songupdate.upload_time = datetime.now()
                db.session.commit()

        if user == AudioTypes(2).name:
            podcastUpdate = podcastInfo.query.filter_by(podcast_id=id).first()
            if not podcastUpdate:
                response = {"status": "Failure"}
                return jsonify(response)
            else:
                print("updating")
                podcastUpdate.podcast_name = receive_update['podcast_name']
                podcastUpdate.podcast_duration = receive_update['podcast_duration']
                podcastUpdate.podcast_upload_time = datetime.now()
                podcastUpdate.podcast_host = receive_update['podcast_host']
                podcastUpdate.podcast_participants = receive_update['podcast_participants']
                db.session.commit()
        if user == AudioTypes(3).name:
            audiobookUpdate = AudiobookInfo.query.filter_by(audiobook_id=id).first()
            if not audiobookUpdate:
                response = {"status": "Failure"}
                return jsonify(response)
            else:
                audiobookUpdate.audiobook_title = receive_update['audiobook_title'],
                audiobookUpdate.audiobook_author = receive_update['audiobook_author'],
                audiobookUpdate.audiobook_duration = receive_update['audiobook_duration'],
                audiobookUpdate.audiobook_upload_time = datetime.now()
                audiobookUpdate.audiobook_narrator = receive_update['audiobook_narrator']

        db.session.commit()

    except Exception as exe:
        print("exception" + str(exe))
        return "Failure", 400
    return "Success",200

@app.route('/<user>', methods=['GET'])
@app.route('/<user>/<int:id>', methods=['GET'])
def get_user(user, id=None):
    try:
        #import pdb; pdb.set_trace()
        if user == AudioTypes(1).name and id is not None:
            objsong = SongInfo.query.filter_by(song_id=id).first()
            if objsong:
                audiofilename = objsong.name
                filepath = 'sounds/' + audiofilename + ".mp3"
                return send_file(filepath, as_attachment=True, attachment_filename=audiofilename)
            else:
                response = {"status": "Failure"}
                return jsonify(response)
        if user == AudioTypes(2).name and id is not None:
            objPodcast = podcastInfo.query.filter_by(podcast_id=id).first()
            if objPodcast:
                audiofilename = objPodcast.podcast_name
                filepath = 'sounds/' + audiofilename + ".mp3"
                return send_file(filepath, as_attachment=True, attachment_filename=audiofilename)
            else:
                response = {"status": "Failure"}
                return jsonify(response)

        if user == AudioTypes(3).name and id is not None:
            objAudiobook = AudiobookInfo.query.filter_by(audiobook_id=id).first()
            if objAudiobook:
                audiofilename = objAudiobook.audiobook_title
                filepath = 'sounds/' + audiofilename + ".mp3"
                return send_file(filepath, as_attachment=True, attachment_filename=audiofilename)
            else:
                response = {"status": "Failure"}
                return jsonify(response)
        if user:
            if user == AudioTypes(1).name:
                print ("songlist")
                songUpdate = SongInfo.query.all()
                getsong_response = get_songlist(songUpdate)
                return jsonify(getsong_response)
            if user == AudioTypes(2).name:
                podUpdate = podcastInfo.query.all()
                getpod_response = get_podlist(podUpdate)
                return jsonify(getpod_response)
            if user == AudioTypes(3).name:
                audioUpdate = AudiobookInfo.query.all()
                getaudio_response = get_audiolist(audioUpdate)
                return jsonify(getaudio_response)

    except Exception as exe:
        print(exe)
        return "Failure", 400
    return "Success",200


@app.route('/<user>/<int:id>', methods=['DELETE'])
def delete_user(user, id):
    try:
        #import pdb; pdb.set_trace()
        #receive_delete = request.get_json()
        if user == AudioTypes(1).name:
            deleteSong = SongInfo.query.filter_by(song_id=id).first()
            print (deleteSong)
            if deleteSong:
                db.session.delete(deleteSong)
            else:
                response = {"status": "Failure"}
                return jsonify(response)
        if user == AudioTypes(2).name:
            deletePodcast = podcastInfo.query.filter_by(podcast_id=id).first()
            if deletePodcast:
                db.session.delete(deletePodcast)
            else:
                response = {"status": "Failure"}
                return jsonify(response)
        if user == AudioTypes(3).name:
            deleteAudiobook = AudiobookInfo.query.filter_by(audiobook_id=id).first()
            if deleteAudiobook:
                db.session.delete(deleteAudiobook)
            else:
                response = {"status": "Failure"}
                return jsonify(response)
        db.session.commit()
    except Exception as exe:
        print(exe)
        return "Failure", 400
    return "Success", 200


if __name__ == '__main__':
    app.run()
