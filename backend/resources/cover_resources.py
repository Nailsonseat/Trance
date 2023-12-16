from flask import request
from flask_restful import Resource, reqparse
from werkzeug import datastructures
import os
from datetime import datetime


class CoverUploadResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'file', type=datastructures.FileStorage, location='files', required=True, help='Image file is required')

    def post(self):
        image_file = request.files['file']

        if image_file:
            # Generate a unique filename using the current timestamp
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{image_file.filename}"

            # Save the file to the assets folder
            upload_path = os.path.join(
                "../src/assets/cover", filename)
            open(upload_path, 'w+')
            image_file.save(upload_path)

            return {
                'message': 'Cover image uploaded successfully',
                'cover_path': upload_path
            }, 201
        else:
            return {'message': 'No image file provided'}, 400
