from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime

from .models import Task
from . import db


tasks = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks"
)


@tasks.route("/", methods=["GET", "POST"])
@login_required
def task_page():

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
        )

        priority = request.form.get(
            "priority",
            "Medium"
        )

        parsed_date = None

        if due_date:

            try:

                parsed_date = datetime.strptime(
                    due_date,
                    "%Y-%m-%d"
                ).date()

            except ValueError:

                flash(
                    "Invalid due date.",
                    category="error"
                )

        if not title:

            flash(
                "Task title cannot be empty.",
                category="error"
            )

        else:

            new_task = Task(
                title=title,
                description=description,
                due_date=parsed_date,
                priority=priority,
                completed=False,
                user_id=current_user.id
            )

            db.session.add(new_task)
            db.session.commit()

            flash(
                "Task added successfully!",
                category="success"
            )

        return redirect(
            url_for("tasks.task_page")
        )

    return render_template(
        "tasks.html",
        user=current_user,
        tasks=get_user_tasks()
    )


def get_user_tasks():

    return Task.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Task.completed.asc(),
        Task.due_date.asc()
    ).all()


# =========================================================
# COMPLETE TASK
# =========================================================

@tasks.route(
    "/complete/<int:task_id>",
    methods=["POST"]
)
@login_required
def complete_task(task_id):

    task = Task.query.get_or_404(
        task_id
    )

    if task.user_id != current_user.id:

        return jsonify({
            "success": False,
            "message": "Unauthorized."
        }), 403

    task.completed = not task.completed

    db.session.commit()

    return jsonify({
        "success": True,
        "completed": task.completed
    })


# =========================================================
# DELETE TASK
# =========================================================

@tasks.route(
    "/delete/<int:task_id>",
    methods=["POST"]
)
@login_required
def delete_task(task_id):

    task = Task.query.get_or_404(
        task_id
    )

    if task.user_id != current_user.id:

        return jsonify({
            "success": False,
            "message": "Unauthorized."
        }), 403

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "success": True
    })