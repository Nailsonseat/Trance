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
def user_login():  # Check if a user is already logged in
    if current_user.is_authenticated:
        return jsonify({"message": "User already logged in", "token": current_user.get_auth_token(), "email": current_user.email})

    data = request.get_json()
    email = data.get('email')
    print("Entered")
    if not email:
        return jsonify({"message": "email not provided"}), 400
    user = user_datastore.find_user(email=email)

    # Check if a user is already logged in
    if current_user.is_authenticated:
        return jsonify({"message": "User already logged in", "token": current_user.get_auth_token(), "email": current_user.email})

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if verify_password(data.get("password"), user.password):
        login_user(user)
        user_datastore.commit()

        return jsonify({"token": user.get_auth_token(), "email": user.email})
    else:
        return jsonify({"message": "Wrong Password"}), 400
