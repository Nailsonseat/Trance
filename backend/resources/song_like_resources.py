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
