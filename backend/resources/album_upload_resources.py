from flask import request, jsonify, make_response
from flask_restful import Resource
from werkzeug.utils import secure_filename
from models import Album
from __init__ import db

UPLOAD_FOLDER = '../src/assets/album'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


class AlbumCoverUploadResource(Resource):
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['file']

        if file.filename == '':
            return {'message': 'No selected file'}, 400

        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}/{filename}")

            cover_path = f"{UPLOAD_FOLDER}/{filename}"
            # Assuming you want to create a new album along with uploading the cover
            response_data = {
                'message': 'Album cover saved successfully',
                'cover_path': cover_path,
            }
            return make_response(jsonify(response_data), 201)

        return {'message': 'Invalid file format'}, 400


class AlbumCoverReplaceResource(Resource):
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def put(self, album_id):
        album = Album.query.get_or_404(album_id)

        if 'file' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['file']

        if file.filename == '':
            return {'message': 'No selected file'}, 400

        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{UPLOAD_FOLDER}/{filename}")

            album.cover_path = f"{UPLOAD_FOLDER}/{filename}"
            db.session.commit()

            return {'message': 'Cover replaced successfully'}

        return {'message': 'Invalid file format'}, 400
