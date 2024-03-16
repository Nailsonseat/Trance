from models import Song, Album, Playlist, PlaylistSong, SongsLiked
from flask_restful import Resource, reqparse, marshal_with, fields
from flask_security import roles_required, auth_required, current_user
from models import db
from datetime import datetime
from resources.fields import song_fields, album_fields
from resources.fields import playlist_fields


class PlaylistListResource(Resource):
    @marshal_with(playlist_fields)
    def get(self):
        playlists = Playlist.query.all()
        return playlists


class PlaylistCreateResource(Resource):
    @marshal_with(playlist_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Name of the playlist is required')
        args = parser.parse_args()

        playlist_name = args['name']

        # Check if a playlist with the same name already exists
        existing_playlist = Playlist.query.filter_by(
            name=playlist_name).first()
        if existing_playlist:
            return {'error': f'Playlist with name {playlist_name} already exists.'}, 400

        # Get the current user ID using authentication logic
        user_id = current_user.id
        if not user_id:
            return {'error': 'User ID not found'}, 401

        # Create a new playlist
        new_playlist = Playlist(name=playlist_name, user_id=user_id)

        # Add the new playlist to the database
        db.session.add(new_playlist)
        db.session.commit()

        return new_playlist, 201


class PlaylistAssignResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'song_ids', type=list, location='json', required=True, help='List of song IDs is required')
        super(PlaylistAssignResource, self).__init__()

    def get(self, playlist_id):
        # Query the database to get the associated song_ids for the given playlist_id
        song_ids = PlaylistSong.query.filter_by(
            playlist_id=playlist_id).with_entities(PlaylistSong.song_id).all()

        # Extract the song_ids from the result
        song_ids = [song_id[0] for song_id in song_ids]

        return {'song_ids': song_ids}

    def put(self, playlist_id):
        # Get the playlist by ID
        playlist = Playlist.query.get_or_404(playlist_id)

        # Parse the request payload using reqparse
        args = self.reqparse.parse_args()
        song_ids = args['song_ids']

        # Remove existing associations for the current playlist
        PlaylistSong.query.filter_by(playlist_id=playlist.id).delete()

        # Create new associations for the given songs and playlist
        for song_id in song_ids:
            playlist_song_association = PlaylistSong(
                song_id=song_id, playlist_id=playlist.id)
            db.session.add(playlist_song_association)

        db.session.commit()

        return {'message': f'Songs assigned to playlist {playlist.name} successfully'}, 200


class PlaylistManagementResource(Resource):
    @marshal_with(playlist_fields)
    # @roles_required('user')
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

    def delete(self, playlist_id):
        # Attempt to find the playlist by its ID
        playlist = Playlist.query.get(playlist_id)

        if not playlist:
            return {'error': 'Playlist not found'}, 404

        # Delete the playlist
        db.session.delete(playlist)
        db.session.commit()

        return {'message': 'Playlist deleted successfully'}, 200
