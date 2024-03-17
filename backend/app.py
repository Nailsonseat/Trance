from flask_security import Security, SQLAlchemyUserDatastore, hash_password, login_user
from models import user_datastore, User, Role, RolesUsers
from datetime import datetime as dt, timedelta
from celery.schedules import crontab
from __init__ import app, db, api, mail
from resources.miscellaneous import AdminDashboardResource, FlagSongResource
from resources.song_resources import SongResource, SongListResource, SongCreateResource, SongManagementResource
from resources.album_resources import AlbumListResource, AlbumCreateResource, AlbumManagementResource, AlbumResource, AlbumAssignResource
from resources.playlist_resources import PlaylistManagementResource, PlaylistListResource, PlaylistAssignResource
from resources.cover_resources import CoverUploadResource
from resources.song_upload_resources import SongUploadResource, SongReplacementResource
from resources.album_upload_resources import AlbumCoverUploadResource, AlbumCoverReplaceResource
from resources.song_like_resources import SongsLikedResource, SongsLikedListResource
from auth.auth import auth_bp
from flask_mail import Mail, Message
from flask import render_template
from tasks import remainder, send_monthly_report
from worker import celery_init_app
celery_app = celery_init_app(app)


@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    app.app_context().push()
    for user in User.query.all():
        role = Role.query.filter_by(id=RolesUsers.query.filter_by(
            id=user.id).first().role_id).first().name
        if role == "user" and user.active == True:
            if (user.last_login_at == None or dt.utcnow()-user.last_login_at > timedelta(days=1)):
                email = user.email
                sender.add_periodic_task(
                    crontab(hour='*', minute='*', day_of_week='*'),
                    # crontab(hour='0', minute='30', day_of_week='*'),
                    remainder.s(email),
                )


@celery_app.on_after_configure.connect
def schedule_monthly_reports(sender, **kwargs):
    for user in User.query.filter_by(role='creator').all():
        sender.add_periodic_task(
            # Run on the 1st day of each month
            crontab(day_of_month='1', hour='0', minute='0'),
            send_monthly_report.s(user),
        )


def initalize_roles():
    admin_role = app.Security.datastore.find_or_create_role(
        name='admin', description='Administrator')
    app.Security.datastore.find_or_create_role(
        name='user', description='User')

    app.Security.datastore.find_or_create_role(
        name='creator', description='Creator')
    db.session.commit()
    if not app.Security.datastore.find_user(username='admin'):
        app.Security.datastore.create_user(
            username='admin', email='admin@gmail.com', password=hash_password('12345678'), roles=[admin_role])
    db.session.commit()


if __name__ == '__main__':

    app.app_context().push()
    db.create_all()

    app.Security = Security(app, user_datastore)

    initalize_roles()

    app.register_blueprint(auth_bp)

    api.add_resource(AdminDashboardResource, '/admin/dashboard')

    api.add_resource(SongListResource, '/songs')
    api.add_resource(AlbumListResource, '/albums')
    api.add_resource(PlaylistListResource, '/playlists')

    api.add_resource(PlaylistManagementResource, '/playlist/<int:playlist_id>')
    api.add_resource(PlaylistAssignResource,
                     '/playlist/<int:playlist_id>/assign')

    api.add_resource(FlagSongResource, '/songs/<int:song_id>/flag')

    api.add_resource(SongResource, '/song/<int:song_id>')
    api.add_resource(SongCreateResource, '/songs/create')

    api.add_resource(CoverUploadResource, '/covers/upload')
    api.add_resource(SongUploadResource, '/songs/upload')

    api.add_resource(SongReplacementResource, '/songs/<int:song_id>/replace')
    api.add_resource(SongManagementResource, '/songs/<int:song_id>/manage')

    api.add_resource(AlbumResource, '/album/<int:album_id>')
    api.add_resource(AlbumCreateResource, '/albums/create')
    api.add_resource(AlbumManagementResource, '/albums/<int:album_id>/manage')
    api.add_resource(AlbumAssignResource, '/albums/<int:album_id>/assign')

    api.add_resource(AlbumCoverUploadResource, '/albumcover/upload')

    api.add_resource(SongsLikedListResource, '/likes/<int:user_id>')
    api.add_resource(SongsLikedResource, '/like/<int:song_id>')

    app.run(debug=True)
