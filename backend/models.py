from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from __init__ import db

base = declarative_base()


class RolesUsers(db.Model, base):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=0)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    lyrics = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    streamed_count = db.Column(db.Integer, default=0)
    reports = db.Column(db.Integer, default=0)
    filepath = db.Column(db.String(255))
    coverpath = db.Column(db.String(255))
    hours = db.Column(db.Integer, default=0)
    minutes = db.Column(db.Integer, default=0)
    seconds = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SongsLiked(db.Model):
    __tablename__ = 'songs_liked'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey(
        'song.id'), unique=True, nullable=False)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.DateTime)
    reports = db.Column(db.Integer, default=0)
    total_hours = db.Column(db.Integer, default=0)
    total_minutes = db.Column(db.Integer, default=0)
    total_seconds = db.Column(db.Integer, default=0)
    cover_path = db.Column(db.String(255))


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class PlaylistSong(db.Model):
    __tablename__ = 'playlist_song'
    playlist_id = db.Column(db.Integer, db.ForeignKey(
        'playlist.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)


class Genres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class SongGenre(db.Model):
    __tablename__ = 'song_genre'
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey(
        'genres.id'), primary_key=True)


class AlbumSong(db.Model):
    __tablename__ = 'song_album'
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey(
        'album.id'), primary_key=True)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
