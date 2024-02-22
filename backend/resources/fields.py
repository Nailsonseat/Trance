from flask_restful import fields

# Define the response format for songs
song_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'artist': fields.String,
    'lyrics': fields.String,
    'likes': fields.Integer,
    'streamed_count': fields.Integer,
    'reports': fields.Integer,
    'album_id': fields.Integer,
    'filepath': fields.String,
    'coverpath': fields.String,
    'created_at': fields.DateTime,
    'genres': fields.List(fields.String),
    'hours': fields.Integer,
    'minutes': fields.Integer,
    'seconds': fields.Integer,
}
# Define the response format for albums
album_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'artist': fields.String,
    'release_date': fields.DateTime,
    'genre': fields.String,
    'reports': fields.Integer,
    'total_hours': fields.Integer,
    'total_minutes': fields.Integer,
    'total_seconds': fields.Integer,
    'cover_path': fields.String,
    'songs': fields.List(fields.Nested(song_fields)),
}

# Define the response format for playlists
playlist_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime,
}
