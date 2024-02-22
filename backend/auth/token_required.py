
from functools import wraps
from flask import jsonify, request
import jwt
from __init__ import app
from models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'auth-token' in request.headers:
            token = request.headers['auth-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(jwt=token,
                              key=app.config['SECRET_KEY'],
                              algorithms=["HS256"])
            current_user = User.query\
                .filter_by(id=data['id'])\
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
            raise
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated
