from flask_security import Security, SQLAlchemyUserDatastore, hash_password, login_user
from models import user_datastore
from __init__ import app, db, api
from resources.miscellaneous import AdminDashboardResource, FlagSongResource
from resources.song_resources import SongResource, SongListResource, SongCreateResource, SongManagementResource
from resources.album_resources import AlbumListResource, AlbumCreateResource, AlbumManagementResource, AlbumResource
from resources.playlist_resources import PlaylistCreateResource, PlaylistManagementResource, PlaylistListResource
from resources.cover_resources import CoverUploadResource
from resources.song_upload_resources import SongUploadResource, SongReplacementResource
from auth.auth import auth_bp


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

    api.add_resource(PlaylistCreateResource, '/playlist/create')
    api.add_resource(PlaylistManagementResource, '/playlist/<int:playlist_id>')
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

    app.run(debug=True)
