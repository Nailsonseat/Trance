from models import Song, Album, Playlist, PlaylistSong, SongsLiked
from flask_restful import Resource, reqparse, marshal_with, fields
from flask_security import roles_required, auth_required
from models import db
from datetime import datetime


class FlagSongResource(Resource):
    @roles_required('user')
    def post(self, song_id):
        song = Song.query.get_or_404(song_id)
        song.reports += 1
        db.session.commit()
        return {'message': 'Song flagged successfully'}


class AdminDashboardResource(Resource):
    def get(self):
        # Logic to retrieve app statistics
        return {'statistics': {'total_users': 100, 'total_creators': 20, 'total_albums': 50}}


# Add resources to the API
