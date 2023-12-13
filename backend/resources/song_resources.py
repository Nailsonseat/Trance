from models import Song, Album, Playlist, PlaylistSong, SongsLiked
from flask_restful import Resource, reqparse, marshal_with, fields, request
from flask_security import roles_required, auth_required
from models import db,  Genres, SongGenre
from datetime import datetime
from resources.fields import song_fields
from __init__ import app
from werkzeug import datastructures
import os
from mutagen.wave import WAVE


class SongResource(Resource):
    @marshal_with(song_fields)
    def get(self, song_id):
        song = Song.query.get_or_404(song_id)
        return song


class SongListResource(Resource):
    @marshal_with(song_fields)
    def get(self):
        songs = Song.query.all()
        return songs


class SongUploadResource(Resource):

    def audio_duration(self, length):
        hours = length // 3600  # calculate in hours
        length %= 3600
        mins = length // 60  # calculate in minutes
        length %= 60
        seconds = length  # calculate in seconds

        return hours, mins, seconds

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

            length = self.audio_duration(int(WAVE(upload_path).info.length))
            return {
                'message': 'File uploaded successfully',
                'file_path': upload_path,
                'duration': {
                    "hours": length[0],
                    "minutes": length[1],
                    "seconds": length[2]
                }
            }, 201
        else:
            return {'message': 'No MP3 file provided'}, 400
