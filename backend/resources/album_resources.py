from models import Song, Album, Playlist, PlaylistSong, SongsLiked
from flask_restful import Resource, reqparse, marshal_with, fields
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
        parser.add_argument('release_date', type=str,
                            required=True, help='Release date is required')
        parser.add_argument('genre', type=str, required=True,
                            help='Genre is required')
        args = parser.parse_args()

        # Logic to create a new album
        new_album = Album(
            title=args['title'],
            artist=args['artist'],
            release_date=args['release_date'],
            genre=args['genre']
        )
        db.session.add(new_album)
        db.session.commit()

        return new_album, 201


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
        db.session.delete(album)
        db.session.commit()
        return {'message': 'Album deleted successfully'}
