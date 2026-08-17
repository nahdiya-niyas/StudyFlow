from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    first_name = db.Column(
        db.String(150),
        nullable=False
    )

    notes = db.relationship(
        "Note",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    tasks = db.relationship(
        "Task",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    study_sessions = db.relationship(
        "StudySession",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Note(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    data = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(50),
        default="General"
    )

    date = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )

    is_pinned = db.Column(
        db.Boolean,
        default=False
    )

    is_favorite = db.Column(
        db.Boolean,
        default=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


class Task(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    due_date = db.Column(
        db.Date
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


class StudySession(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    subject = db.Column(
        db.String(200),
        nullable=False
    )

    study_date = db.Column(
        db.Date,
        nullable=False
    )

    start_time = db.Column(
        db.String(20)
    )

    duration = db.Column(
        db.Integer,
        default=60
    )

    notes = db.Column(
        db.String(1000)
    )

    status = db.Column(
        db.String(20),
        default='planned'
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )