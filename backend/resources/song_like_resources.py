from models import SongsLiked
from flask_restful import Resource
from flask import jsonify
from models import SongsLiked
from __init__ import db
from flask_restful import Resource, reqparse


class SongsLikedListResource(Resource):
    def get(self, user_id):
        songs_liked = SongsLiked.query.filter_by(user_id=user_id).all()
        return jsonify([song_liked.song_id for song_liked in songs_liked])


class SongsLikedResource(Resource):
    def get(self, song_id):
        songs_liked = SongsLiked.query.filter_by(song_id=song_id).all()
        return jsonify([song_liked.user_id for song_liked in songs_liked])

    def put(self, song_id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, required=True)
        args = parser.parse_args()
        song_liked = SongsLiked.query.filter_by(
            song_id=song_id, user_id=args['user_id']).first()

        print(song_liked)
        if song_liked:
            db.session.delete(song_liked)
            db.session.commit()
            return jsonify({'message': 'Song unliked'})
        else:
            song_liked = SongsLiked(song_id=song_id, user_id=args['user_id'])
            db.session.add(song_liked)
            db.session.commit()
            return jsonify({'message': 'Song liked'})
