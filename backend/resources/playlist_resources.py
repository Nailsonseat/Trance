from models import Song, Album, Playlist, PlaylistSong, SongsLiked
from flask_restful import Resource, reqparse, marshal_with, fields
from flask_security import roles_required, auth_required
from models import db
from datetime import datetime
from resources.fields import song_fields, album_fields
from resources.fields import playlist_fields


class PlaylistCreateResource(Resource):
    @roles_required('user')
    @marshal_with(playlist_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Name of the playlist is required')
        parser.add_argument('songs', type=list, required=True,
                            help='List of song IDs is required')
        args = parser.parse_args()

        playlist_name = args['name']
        song_ids = args['songs']

        existing_playlist = Playlist.query.filter_by(
            name=playlist_name).first()
        if existing_playlist:
            return {'error': f'Playlist with name {playlist_name} already exists.'}, 400

        songs = Song.query.filter(Song.id.in_(song_ids)).all()
        if len(songs) != len(song_ids):
            return {'error': 'One or more provided song IDs are invalid.'}, 400

        # Get the current user ID
        user_id = getattr(auth_required.current_user, 'id', None)
        if not user_id:
            return {'error': 'User ID not found'}, 401

        new_playlist = Playlist(name=playlist_name, user_id=user_id)

        # Link the playlist with songs through the SongsLiked table
        for song in songs:
            new_playlist.songs.append(song)

        db.session.add(new_playlist)
        db.session.commit()

        return new_playlist, 201


class PlaylistManagementResource(Resource):
    @marshal_with(playlist_fields)
    @roles_required('user')
    def put(self, playlist_id):
        parser = reqparse.RequestParser()
        parser.add_argument('songs_to_add', type=list,
                            help='List of song IDs to add to the playlist')
        parser.add_argument('songs_to_remove', type=list,
                            help='List of song IDs to remove from the playlist')
        args = parser.parse_args()

        playlist = Playlist.query.get_or_404(playlist_id)

        if args['songs_to_add']:
            songs_to_add = Song.query.filter(
                Song.id.in_(args['songs_to_add'])).all()

            # Link the playlist with added songs through the SongsLiked table
            for song in songs_to_add:
                if song not in playlist.songs:
                    playlist.songs.append(song)

        if args['songs_to_remove']:
            songs_to_remove = Song.query.filter(
                Song.id.in_(args['songs_to_remove'])).all()

            # Unlink the playlist from removed songs through the SongsLiked table
            for song in songs_to_remove:
                if song in playlist.songs:
                    playlist.songs.remove(song)

        db.session.commit()

        return playlist

