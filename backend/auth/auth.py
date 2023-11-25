from flask import Blueprint, jsonify, request
from flask_security import verify_password, current_user, login_user
from werkzeug.security import check_password_hash
from flask_restful import Resource, Api, reqparse, fields
from models import user_datastore
from __init__ import app


auth_bp = Blueprint('auth', __name__)
api = Api(auth_bp)

register_fields = {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String
}

register_parser = reqparse.RequestParser()
for field, field_type in register_fields.items():
    register_parser.add_argument(field, type=field_type)

login_fields = {
    'email': fields.String,
    'password': fields.String
}

login_parser = reqparse.RequestParser()
for field, field_type in login_fields.items():
    login_parser.add_argument(field, type=field_type)


@auth_bp.post('/login-user')
def login_user():
    response = request.get_json()
    email = response.get('email')
    if not email:
        return jsonify({"message": "email not provided"}), 400

    user = user_datastore.find_user(email=email, role='user')

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if verify_password(response.get("password"), user.password):
        login_user(user)
        user.last_login_time = datetime.utcnow()
        user_datastore.commit()
        db.session.commit()

        print("Sucessfully logged in")

        return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name})
    else:
        return jsonify({"message": "FAILURE"}), 400
