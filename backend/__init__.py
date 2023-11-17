from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'f724f39fcae64ca2ba988bf09ee91c66'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECURITY_LOGIN_URL'] = '/login'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'auth'
app.config['SECURITY_TOKEN_AUTHENTICATION_KEY'] = 'Authorization'
app.config['SECURITY_TOKEN_MAX_AGE'] = 3600
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_TOKEN_URL'] = '/token'
app.config['SECURITY_EMAIL_DOMAIN'] = 'gmail.com'
app.config['SECURITY_USERNAME'] = True
app.config['SECURITY_USERNAME_REQUIRED'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_POST_LOGIN_VIEW'] = '/protected'
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/login'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_REGISTER_USERNAME'] = True
app.config['SECURITY_DEFAULT_ROLES'] = 'user'


db = SQLAlchemy(app)
# migrate = Migrate(app, db)
api = Api(app, prefix="/api/v1")
