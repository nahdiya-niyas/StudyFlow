from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(app.instance_path, DB_NAME)}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Make sure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize database
    db.init_app(app)

    # Import blueprints
    from .views import views
    from .auth import auth
    from .tasks import tasks
    from .planner import planner

    # Register blueprints
    app.register_blueprint(views)
    app.register_blueprint(auth)
    app.register_blueprint(tasks)
    app.register_blueprint(planner)

    # Import models and create database
    from .models import User, Note, Task, StudySession

    with app.app_context():
        db.create_all()

    # Flask-Login
    login_manager = LoginManager()

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "error"

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app