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

