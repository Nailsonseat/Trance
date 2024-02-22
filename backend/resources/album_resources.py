from flask_restful import Resource, reqparse
from models import AlbumSong, Song, Album, Playlist, PlaylistSong, SongsLiked
from flask_restful import Resource, reqparse, marshal_with, fields, request
from flask_security import roles_required, auth_required
from models import db
from datetime import datetime
from resources.fields import song_fields, album_fields


class AlbumResource(Resource):
    @marshal_with(album_fields)
    def get(self, album_id):
        album = Album.query.get_or_404(album_id)
        # Fetch associated songs for the album
        songs = Song.query.filter_by(album_id=album_id).all()
        album.songs = songs
        return album


class AlbumListResource(Resource):
    @marshal_with(album_fields)
    def get(self):
        albums = Album.query.all()
        return albums


class AlbumCreateResource(Resource):
    @marshal_with(album_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True,
                            help='Album title is required')
        parser.add_argument('artist', type=str, required=True,
                            help='Artist name is required')
        parser.add_argument('cover_path', type=str)
        args = parser.parse_args()

        # Logic to create a new album
        new_album = Album(
            title=args['title'],
            artist=args['artist'],
            release_date=datetime.utcnow(),
            cover_path=args['cover_path'],
            total_hours=0,
            total_minutes=0,
            total_seconds=0
        )
        db.session.add(new_album)
        db.session.commit()

        return new_album, 201


class AlbumAssignResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'song_ids', type=list, location='json', required=True, help='List of song IDs is required')
        super(AlbumAssignResource, self).__init__()

    def get(self, album_id):
        # Query the database to get the associated song_ids for the given album_id
        song_ids = AlbumSong.query.filter_by(
            album_id=album_id).with_entities(AlbumSong.song_id).all()

        # Extract the song_ids from the result
        song_ids = [song_id[0] for song_id in song_ids]

        return {'song_ids': song_ids}

    def put(self, album_id):
        # Get the album by ID
        album = Album.query.get_or_404(album_id)

        # Parse the request payload using reqparse
        args = self.reqparse.parse_args()
        song_ids = args['song_ids']

        # Remove existing associations for the current album
        AlbumSong.query.filter_by(album_id=album.id).delete()

        album.total_hours = 0
        album.total_minutes = 0
        album.total_seconds = 0

        # Create new associations for the given songs and album
        for song_id in song_ids:
            song_album_association = AlbumSong(
                song_id=song_id, album_id=album.id)
            # Update the total time of the album
            song = Song.query.get(song_id)
            album.total_hours += song.hours
            album.total_minutes += song.minutes
            album.total_seconds += song.seconds
            db.session.add(song_album_association)

        db.session.commit()

        return {'message': f'Songs assigned to album {album.title} successfully'}, 200


class AlbumManagementResource(Resource):
    @marshal_with(album_fields)
    def put(self, album_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help='Album title')
        parser.add_argument('artist', type=str, help='Artist name')
        parser.add_argument('release_date', type=str, help='Release date')
        parser.add_argument('genre', type=str, help='Genre')
        args = parser.parse_args()

        # Logic to update an existing album
        album = Album.query.get_or_404(album_id)

        if args['title']:
            album.title = args['title']
        if args['artist']:
            album.artist = args['artist']
        if args['release_date']:
            album.release_date = args['release_date']
        if args['genre']:
            album.genre = args['genre']

        db.session.commit()

        return album

    def delete(self, album_id):
        album = Album.query.get_or_404(album_id)
        AlbumSong.query.filter_by(album_id=album_id).delete()
        db.session.delete(album)
        db.session.commit()
        return {'message': 'Album deleted successfully'}
