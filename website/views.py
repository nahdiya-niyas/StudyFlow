from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    jsonify
)

from flask_login import login_required, current_user

from .models import Note, Task, StudySession
from . import db


views = Blueprint("views", __name__)


# =========================================================
# DASHBOARD
# =========================================================

@views.route("/")
@login_required
def home():

    notes = Note.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Note.date.desc()
    ).all()

    pending_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).count()

    completed_tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).count()

    tasks = Task.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(
        Task.due_date.asc()
    ).limit(5).all()

    study_sessions = StudySession.query.filter_by(
        user_id=current_user.id
    ).order_by(
        StudySession.study_date.asc()
    ).limit(4).all()

    return render_template(
        "dashboard.html",
        user=current_user,
        notes=notes,
        tasks=tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        study_sessions=study_sessions
    )


# =========================================================
# NOTES
# =========================================================

@views.route("/notes", methods=["GET", "POST"])
@login_required
def notes():

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        note_data = request.form.get(
            "note",
            ""
        ).strip()

        category = request.form.get(
            "category",
            "General"
        ).strip()

        if not title:

            flash(
                "Please enter a note title.",
                category="error"
            )

        elif not note_data:

            flash(
                "Note content cannot be empty.",
                category="error"
            )

        else:

            new_note = Note(
                title=title,
                data=note_data,
                category=category or "General",
                user_id=current_user.id
            )

            db.session.add(new_note)
            db.session.commit()

            flash(
                "Note created successfully!",
                category="success"
            )

            return redirect(
                url_for("views.notes")
            )

    user_notes = Note.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Note.is_pinned.desc(),
        Note.date.desc()
    ).all()

    return render_template(
        "notes.html",
        user=current_user,
        notes=user_notes
    )


# =========================================================
# READ NOTE
# =========================================================

@views.route("/note/<int:note_id>")
@login_required
def read_note(note_id):

    note = Note.query.get_or_404(note_id)

    # Make sure users can only read their own notes
    if note.user_id != current_user.id:

        flash(
            "You cannot view this note.",
            category="error"
        )

        return redirect(
            url_for("views.notes")
        )

    return render_template(
        "read_note.html",
        user=current_user,
        note=note
    )


# =========================================================
# EDIT NOTE
# =========================================================

@views.route(
    "/edit-note/<int:note_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_note(note_id):

    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:

        flash(
            "You cannot edit this note.",
            category="error"
        )

        return redirect(
            url_for("views.notes")
        )

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        note_data = request.form.get(
            "note",
            ""
        ).strip()

        category = request.form.get(
            "category",
            "General"
        ).strip()

        if not title or not note_data:

            flash(
                "Title and note content are required.",
                category="error"
            )

            return render_template(
                "edit_note.html",
                user=current_user,
                note=note
            )

        note.title = title
        note.data = note_data
        note.category = category or "General"

        db.session.commit()

        flash(
            "Note updated successfully!",
            category="success"
        )

        return redirect(
            url_for(
                "views.read_note",
                note_id=note.id
            )
        )

    return render_template(
        "edit_note.html",
        user=current_user,
        note=note
    )


# =========================================================
# DELETE NOTE
# =========================================================

@views.route(
    "/delete-note",
    methods=["POST"]
)
@login_required
def delete_note():

    data = request.get_json(
        silent=True
    ) or {}

    note_id = data.get("noteId")

    if not note_id:

        return jsonify({
            "success": False,
            "message": "Note ID is missing."
        }), 400

    note = Note.query.get(note_id)

    if not note:

        return jsonify({
            "success": False,
            "message": "Note not found."
        }), 404

    if note.user_id != current_user.id:

        return jsonify({
            "success": False,
            "message": "Unauthorized."
        }), 403

    db.session.delete(note)
    db.session.commit()

    return jsonify({
        "success": True
    })


# =========================================================
# PIN NOTE
# =========================================================

@views.route(
    "/toggle-pin/<int:note_id>",
    methods=["POST"]
)
@login_required
def toggle_pin(note_id):

    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:

        return jsonify({
            "success": False,
            "message": "Unauthorized."
        }), 403

    note.is_pinned = not note.is_pinned

    db.session.commit()

    return jsonify({
        "success": True,
        "pinned": note.is_pinned
    })


# =========================================================
# FAVORITE NOTE
# =========================================================

@views.route(
    "/toggle-favorite/<int:note_id>",
    methods=["POST"]
)
@login_required
def toggle_favorite(note_id):

    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id:

        return jsonify({
            "success": False,
            "message": "Unauthorized."
        }), 403

    note.is_favorite = not note.is_favorite

    db.session.commit()

    return jsonify({
        "success": True,
        "favorite": note.is_favorite
    })


# =========================================================
# TASKS
# =========================================================

@views.route(
    "/tasks",
    methods=["GET", "POST"]
)
@login_required
def tasks():

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        due_date = request.form.get(
            "due_date",
            ""
        ).strip()

        priority = request.form.get(
            "priority",
            "Medium"
        ).strip()

        if not title:

            flash(
                "Please enter a task title.",
                category="error"
            )

        else:

            new_task = Task(
                title=title,
                description=description,
                due_date=due_date if due_date else None,
                priority=priority or "Medium",
                completed=False,
                user_id=current_user.id
            )

            db.session.add(new_task)
            db.session.commit()

            flash(
                "Task created successfully!",
                category="success"
            )

            return redirect(
                url_for("views.tasks")
            )

    user_tasks = Task.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Task.completed.asc(),
        Task.due_date.asc()
    ).all()

    return render_template(
        "tasks.html",
        user=current_user,
        tasks=user_tasks
    )


# =========================================================
# PLANNER
# =========================================================

@views.route(
    "/planner",
    methods=["GET", "POST"]
)
@login_required
def planner():

    if request.method == "POST":

        subject = request.form.get(
            "subject",
            ""
        ).strip()

        study_date = request.form.get(
            "study_date",
            ""
        ).strip()

        start_time = request.form.get(
            "start_time",
            ""
        ).strip()

        duration = request.form.get(
            "duration",
            "60"
        ).strip()

        session_notes = request.form.get(
            "notes",
            ""
        ).strip()

        if not subject:

            flash(
                "Please enter a subject.",
                category="error"
            )

        elif not study_date:

            flash(
                "Please select a study date.",
                category="error"
            )

        else:

            try:
                duration_value = int(duration)
            except (ValueError, TypeError):
                duration_value = 60

            new_session = StudySession(
                subject=subject,
                study_date=study_date,
                start_time=start_time,
                duration=duration_value,
                notes=session_notes,
                status="planned",
                user_id=current_user.id
            )

            db.session.add(new_session)
            db.session.commit()

            flash(
                "Study session added successfully!",
                category="success"
            )

            return redirect(
                url_for("views.planner")
            )

    sessions = StudySession.query.filter_by(
        user_id=current_user.id
    ).order_by(
        StudySession.study_date.asc()
    ).all()

    return render_template(
        "planner.html",
        user=current_user,
        study_sessions=sessions
    )


# =========================================================
# PROFILE
# =========================================================

@views.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html",
        user=current_user
    )