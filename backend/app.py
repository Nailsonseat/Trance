from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from models import db, user_datastore
from __init__ import app
from auth.auth import auth_bp


def initalize_roles():
    admin_role = app.Security.datastore.find_or_create_role(
        name='admin', description='Administrator')
    app.Security.datastore.find_or_create_role(
        name='user', description='User')
    if not app.Security.datastore.find_user(username='Admin'):
        app.Security.datastore.create_user(
            username='Admin', email='admin@gmail.com', password=hash_password('12345678'), roles=[admin_role])


if __name__ == '__main__':

    app.app_context().push()
    db.create_all()

    app.Security = Security(app, user_datastore)

    initalize_roles()

    app.register_blueprint(auth_bp)
    db.session.commit()
    app.run(debug=True)
