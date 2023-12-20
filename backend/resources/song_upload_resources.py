from werkzeug.datastructures import FileStorage
from models import Song
from flask_restful import Resource
from models import Song, Album, Playlist, PlaylistSong, SongsLiked
from flask_restful import Resource, reqparse, marshal_with, fields, request
from flask_security import roles_required, auth_required
from flask import jsonify, make_response
from models import db,  Genres, SongGenre
from datetime import datetime
from resources.fields import song_fields
from __init__ import app
from werkzeug import datastructures
import os
from mutagen.mp3 import MP3


def audio_duration(length):
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds

    return hours, mins, seconds


class SongUploadResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'file', type=datastructures.FileStorage, location='files', required=True, help='MP3 file is required')

    def post(self):

        mp3_file = request.files['file']

        if mp3_file:
            # Generate a unique filename using the current timestamp
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{mp3_file.filename}"

            # Save the file to the assets folder
            upload_path = os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            open(upload_path, 'w+')
            mp3_file.save(upload_path)
            response_data = {}
            audio = MP3(upload_path)

            # contains all the metadata about the wavpack file
            audio_info = audio.info
            length = int(audio_info.length)
            hours, minutes, seconds = audio_duration(length)

            response_data = {
                'message': 'File uploaded successfully',
                'file_path': upload_path,
                'duration': {
                    "hours": hours,
                    "minutes": minutes,
                    "seconds": seconds
                }
            }
            return make_response(jsonify(response_data), 201)
        else:
            return {'message': 'No MP3 file provided'}, 400


class SongReplacementResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'file', type=FileStorage, location='files', required=True, help='MP3 file is required')

    def put(self, song_id):
        song = Song.query.get_or_404(song_id)
        mp3_file = request.files['file']

        if mp3_file:
            # Generate a unique filename using the current timestamp
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{mp3_file.filename}"

            # Save the file to the assets folder
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            open(upload_path, 'w+')
            mp3_file.save(upload_path)
            response_data = {}
            audio = MP3(upload_path)

            # contains all the metadata about the mp3 file
            audio_info = audio.info
            length = int(audio_info.length)
            hours, minutes, seconds = audio_duration(length)

            # Update the song information in the database
            song.filepath = upload_path
            song.hours = hours
            song.minutes = minutes
            song.seconds = seconds

            db.session.commit()

            response_data = {
                'message': 'File replaced successfully',
                'file_path': upload_path,
                'duration': {
                    "hours": hours,
                    "minutes": minutes,
                    "seconds": seconds
                }
            }
            return make_response(jsonify(response_data), 200)
        else:
            return {'message': 'No MP3 file provided'}, 400
