from flask import Flask
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'f724f39f4206964ca2ba1238bf09ee91c99'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'f724f39fcae64ca2ba988bf09ee91c99'
app.config['SECURITY_REGISTERABLE'] = True
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "aadarshv3@gmail.com"
app.config['UPLOAD_FOLDER'] = "../src/assets/music"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PASSWORD'] = "qeydzqnwlojcdoxc"

db = SQLAlchemy(app)

api = Api(app, prefix="")
mail = Mail(app)
