from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

DB_NAME = "database.db"


def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'change-this-secret-key'

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'sqlite:///{DB_NAME}'
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    from .views import views
    from .auth import auth
    from .tasks import tasks
    from .planner import planner


    app.register_blueprint(
        views,
        url_prefix='/'
    )

    app.register_blueprint(
        auth,
        url_prefix='/'
    )

    app.register_blueprint(
        tasks
    )

    app.register_blueprint(
        planner
    )


    from .models import (
        User,
        Note,
        Task,
        StudySession
    )


    with app.app_context():

        db.create_all()


    login_manager = LoginManager()

    login_manager.login_view = 'auth.login'

    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(
            int(user_id)
        )


    return app