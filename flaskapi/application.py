from flask import Flask, request, jsonify, send_file
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from Models.model import *
from datetime import datetime


#now = datetime.now()


application = app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sanket:apple@123@localhost:3305/db'
#app.config['SQLALCHEMY_ECHO'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///UserInfo.sqlite3'
db = SQLAlchemy(app)


@app.route('/<user>', methods=['POST'])
def create_user(user):
    #import pdb;pdb.set_trace()
    try:
        print(datetime.now())
        x = datetime.now()
        print(user)
        receive_data = request.get_json()
        print(receive_data)
        userdata = request.data
        usdata = userdata.decode('ascii')
        print(usdata)
        print (receive_data['user_id'])
        if user == AudioTypes(1).name:
            print("In song")
            songIn = SongInfo.query.filter_by(user_id=receive_data['user_id']).first()
            if (songIn):
                response = {"status":"Failure", "msg": "Song already exist"}
                return jsonify(response)
            else:
                add_data = SongInfo(user_id=receive_data['user_id'], name=receive_data['name'],
                                    duration=receive_data['duration'], upload_time=datetime.now())
        if user == AudioTypes(2).name:
            podcastIn = podcastInfo.query.filter_by(podcast_id=receive_data['podcast_id']).first()
            if (podcastIn):
                response = {"status": "Failure", "msg": "podcast already exist"}
                return jsonify(response)
            else:
                add_data = podcastInfo(podcast_id=receive_data['podcast_id'], podcast_name=receive_data['podcast_name'],
                                    podcast_duration=receive_data['podcast_duration'], upload_time=datetime.now(),podcast_host=receive_data['podcast_host'],
                                       podcast_participants=receive_data['podcast_participants'])
        if user == AudioTypes(3).name:
            audiobookIn =  AudiobookInfo.query.filter_by(audiobook_id=receive_data['audiobook_id']).first()
            if (audiobookIn):
                pass
            else:
                add_data = AudiobookInfo(audiobook_id=receive_data['audiobook_id'], audiobook_title=receive_data['audiobook_title'],
                                         audiobook_author=receive_data['audiobook_author'],audiobook_duration=receive_data['audiobook_duration'],
                                         upload_time=datetime.now(), audiobook_narrator=receive_data['audiobook_narrator'])

        db.session.add(add_data)
        db.session.commit()

        #print (SongInfo.query.all)
        #print(SongInfo.query.all())
        #print (request.args['user_id'])
    except Exception as exe:
        print (exe)
        return "Failure",400
    return "Success",200

@app.route('/<user>/<int:id>', methods=['PUT'])
def update_user(user,id):
    #import pdb;pdb.set_trace()
    receive_update = request.get_json()
    if user == AudioTypes(1).name:
        print("update")
        songupdate = SongInfo.query.filter_by(user_id = id).first()
        if not songupdate:
            return ("failed")
        else:
            songupdate.name =receive_update['name']
            songupdate.duration = receive_update['duration']
            songupdate.upload_time = datetime.now()
            #db.session.add(songupdate)
            db.session.commit()
            #update_data = SongInfo(name=receive_update['name'],
                                #duration=receive_update['duration'], upload_time=datetime.now())
            #SongInfo.query.filter_by(user_id=receive_update['user_id']).update()
    if user == 2:
        if (podcastInfo.query.filter_by(user_id = receive_update['podcast_id']).first()):
            return ("failed")
        else:
            add_podcast = podcastInfo(podcast_id=receive_update['podcast_id'], podcast_name=receive_update['podcast_name'],
                                   podcast_duration=receive_update['podcast_duration'], upload_time=datetime.now(),
                                   podcast_host=receive_update['podcast_host'],
                                   podcast_participants=receive_update['podcast_participants'])
            podcastInfo.query.filter_by(podcast_id=receive_update['podcast_id']).update(add_podcast)
    if user == 3:
        if (AudiobookInfo.query.filter_by(user_id = receive_update['audiobook_id']).first()):
            return ("failed")
        else:
            add_audiobook = AudiobookInfo(audiobook_id=receive_data['audiobook_id'],
                                     audiobook_title=receive_data['audiobook_title'],
                                     audiobook_author=receive_data['audiobook_author'],
                                     audiobook_duration=receive_data['audiobook_duration'],
                                     upload_time=datetime.now(), audiobook_narrator=receive_data['audiobook_narrator'])
            AudiobookInfo.query.filter_by(audiobook_id=receive_update['audiobook_id']).update(add_audiobook)
    #db.session.add()
    db.session.commit()
    return ("success")

@app.route('/<user>/<int:id>', methods=['GET'])
def get_user(user,id):
    objname = SongInfo.query.filter_by(user_id=id).first()
    if (objname):
        audiofilename = objname.name
        filepath = 'sounds/'+audiofilename + ".mp3"
        return send_file(filepath,as_attachment = True, attachment_filename=audiofilename)

@app.route('/<user>/<int:id>', methods=['DELETE'])
def delete_user(user,id):
    receive_delete = request.get_json()
    if user == 1:
        if (SongInfo.query.filter_by(user_id =receive_delete['user_id']).first()):
            delete_record = SongInfo.query.filter_by(user_id =receive_delete['user_id']).first()
    if user == 2:
        if (podcastInfo.query.filter_by(podcast_id = receive_delete['podcast_id']).first()):
            delete_record = podcastInfo.query.filter_by(podcast_id=receive_delete['podcast_id']).first()
    if user == 3:
        if (AudiobookInfo.query.filter_by(audiobook_id=receive_delete['audiobook_id']).first()):
            delete_record = AudiobookInfo.query.filter_by(audiobook_id=receive_delete['audiobook_id']).first()
    db.session.delete(delete_record)
    db.session.commit()
    return ("success")


if __name__ == '__main__':
    app.run()