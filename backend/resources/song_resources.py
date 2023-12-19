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
            response_data = {}
            audio = MP3(upload_path)

            # contains all the metadata about the wavpack file
            audio_info = audio.info
            length = int(audio_info.length)
            hours, minutes, seconds = self.audio_duration(length)

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


class SongCreateResource(Resource):
    @marshal_with(song_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True,
                            help='Title is required')
        parser.add_argument('artist', type=str, required=True,
                            help='Artist is required')
        parser.add_argument('lyrics', type=str, required=True,
                            help='Lyrics are required')
        parser.add_argument('album_id', type=int, help='Album ID')
        parser.add_argument('filepath', type=str,
                            help='Path where mp3 is stored')
        args = parser.parse_args()

        # Fill in the created_at with the current time
        args['created_at'] = datetime.utcnow()

        # Logic to create a new song
        new_song = Song(
            title=args['title'],
            artist=args['artist'],
            lyrics=args['lyrics'],
            album_id=args['album_id'],
            filepath=args['filepath'],
            created_at=args['created_at']
        )

        db.session.add(new_song)
        db.session.commit()

        # Handling genre assignment
        genres = request.json.get('genres', [])
        for genre_name in genres:
            genre = Genres.query.filter_by(name=genre_name).first()
            if genre is None:
                genre = Genres(name=genre_name)
                db.session.add(genre)
                db.session.commit()

            song_genre = SongGenre(song_id=new_song.id, genre_id=genre.id)
            db.session.add(song_genre)

        db.session.commit()

        return new_song, 201


class SongManagementResource(Resource):
    @marshal_with(song_fields)
    def put(self, song_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('lyrics', type=str)
        parser.add_argument('genres', type=list)
        args = parser.parse_args()

        song = Song.query.get_or_404(song_id)

        # Remove existing genre associations
        SongGenre.query.filter_by(song_id=song.id).delete()

        # Commit the changes to the database
        db.session.commit()

        # Add new genre associations
        new_genres = []

        for genre_name in args['genres']:
            # Check if the genre already exists
            genre = Genres.query.filter_by(name=genre_name).first()
            if not genre:
                # If the genre doesn't exist, create a new one
                genre = Genres(name=genre_name)
                db.session.add(genre)
                db.session.commit()

            # Create a SongGenre association
            song_genre = SongGenre(song_id=song.id, genre_id=genre.id)
            new_genres.append(song_genre)

        # Add the new genre associations to the SongGenre table
        db.session.bulk_save_objects(new_genres)

        # Commit the changes to the database
        db.session.commit()

        return song

    def delete(self, song_id):
        song = Song.query.get_or_404(song_id)
        db.session.delete(song)
        db.session.commit()

        return {'message': 'Song deleted successfully'}
