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
    'created_at': fields.DateTime,
    'genres': fields.List(fields.String),
}

# Define the response format for albums
album_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'artist': fields.String,
    'release_date': fields.DateTime,
    'genre': fields.String,
    'reports': fields.Integer,
    'cover_path': fields.String,
    'songs': fields.List(fields.Nested(song_fields)),
}

