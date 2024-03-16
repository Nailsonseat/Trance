from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_security import verify_password, hash_password, logout_user, auth_required, roles_required, login_user, current_user
from auth.token_required import token_required
from models import User, user_datastore
from __init__ import app, db
from functools import wraps
import jwt
from tasks import send_welcome


auth_bp = Blueprint('auth', __name__)


@app.get('/admin')
@auth_required("token")
@roles_required("admin")
def admin():
    return "Hello Admin"


@auth_bp.post('/login-user')
def user_login():
    response = request.get_json()
    email = response.get('email')

    if not email:
        return jsonify({"message": "email not provided"}), 400

    user = user_datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if verify_password(response.get("password"), user.password) and user.roles[0].name == response.get("role"):
        login_user(user)
        user.last_login_time = datetime.utcnow()
        user_datastore.commit()
        db.session.commit()

        token = jwt.encode(
            {"id": user.id, "role": user.roles[0].name, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({"token": token, "username": user.username, "email": user.email, "role": user.roles[0].name, "id": user.id})
    else:
        return jsonify({"message": "FAILURE"}), 400


@auth_bp.post('/register-user')
def register_user():
    response = request.get_json()
    username = response.get('username')
    email = response.get('email')
    password = response.get('password')
    role = response.get('role')

    try:
        print(user_datastore.find_user(email=email))
        if not user_datastore.find_user(email=email):
            user_datastore.create_user(
                username=username, email=email, password=hash_password(password), roles=[role])
        db.session.commit()
        send_welcome(email)
        return jsonify({"message": "SUCCESS"}), 200
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"


@auth_bp.get('/logout-user')
@token_required
def logout(user):
    user.last_loggout_time = datetime.utcnow()
    logout_user()
    db.session.commit()
    return jsonify({'message': 'Logout Sucessful'})
