from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import StudySession
from . import db
from datetime import datetime


planner = Blueprint(
    'planner',
    __name__,
    url_prefix='/planner'
)


# =========================================================
# GET USER SESSIONS
# =========================================================

def get_sessions():

    return StudySession.query.filter_by(
        user_id=current_user.id
    ).order_by(
        StudySession.study_date.asc(),
        StudySession.start_time.asc()
    ).all()


# =========================================================
# PLANNER PAGE
# =========================================================

@planner.route('/', methods=['GET', 'POST'])
@login_required
def study_planner():

    if request.method == 'POST':

        subject = request.form.get(
            'subject',
            ''
        ).strip()

        study_date = request.form.get(
            'study_date',
            ''
        ).strip()

        start_time = request.form.get(
            'start_time',
            ''
        ).strip()

        duration = request.form.get(
            'duration',
            ''
        ).strip()

        notes = request.form.get(
            'notes',
            ''
        ).strip()


        # -------------------------------------------------
        # PARSE DATE
        # -------------------------------------------------

        parsed_date = None

        if study_date:

            try:

                parsed_date = datetime.strptime(
                    study_date,
                    '%Y-%m-%d'
                ).date()

            except ValueError:

                parsed_date = None


        # -------------------------------------------------
        # PARSE DURATION
        # -------------------------------------------------

        try:

            session_duration = int(duration)

        except (ValueError, TypeError):

            session_duration = 60


        if session_duration <= 0:

            session_duration = 1


        # -------------------------------------------------
        # CREATE SESSION
        # -------------------------------------------------

        if subject and parsed_date:

            new_session = StudySession(

                subject=subject,

                study_date=parsed_date,

                start_time=start_time
                if start_time
                else None,

                duration=session_duration,

                notes=notes,

                status='planned',

                user_id=current_user.id

            )

            db.session.add(new_session)

            db.session.commit()


        # -------------------------------------------------
        # REDIRECT AFTER POST
        # -------------------------------------------------

        return redirect(
            url_for(
                'planner.study_planner'
            )
        )


    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    return render_template(
        'planner.html',
        user=current_user,
        sessions=get_sessions()
    )


# =========================================================
# START SESSION
# =========================================================

@planner.route(
    '/start/<int:session_id>',
    methods=['POST']
)
@login_required
def start_session(session_id):

    session = StudySession.query.filter_by(
        id=session_id,
        user_id=current_user.id
    ).first()


    if not session:

        return jsonify({
            'success': False,
            'message': 'Session not found.'
        }), 404


    if session.status == 'completed':

        return jsonify({
            'success': False,
            'message': 'This session has already been completed.'
        }), 400


    session.status = 'active'

    db.session.commit()


    return jsonify({

        'success': True,

        'session_id': session.id,

        'duration': int(
            session.duration
        ),

        'message': 'Study session started!'

    })


# =========================================================
# COMPLETE SESSION
# =========================================================

@planner.route(
    '/complete/<int:session_id>',
    methods=['POST']
)
@login_required
def complete_session(session_id):

    session = StudySession.query.filter_by(
        id=session_id,
        user_id=current_user.id
    ).first()


    if not session:

        return jsonify({
            'success': False,
            'message': 'Session not found.'
        }), 404


    # -----------------------------------------------------
    # ALREADY COMPLETED
    # -----------------------------------------------------

    if session.status == 'completed':

        return jsonify({

            'success': True,

            'session_id': session.id,

            'already_completed': True,

            'message': 'Session was already completed.'

        })


    # -----------------------------------------------------
    # COMPLETE
    # -----------------------------------------------------

    session.status = 'completed'

    db.session.commit()


    return jsonify({

        'success': True,

        'session_id': session.id,

        'already_completed': False,

        'message': '🎉 Session completed! Great work!'

    })


# =========================================================
# DELETE SESSION
# =========================================================

@planner.route(
    '/delete/<int:session_id>',
    methods=['POST']
)
@login_required
def delete_session(session_id):

    session = StudySession.query.filter_by(
        id=session_id,
        user_id=current_user.id
    ).first()


    if not session:

        return jsonify({
            'success': False,
            'message': 'Session not found.'
        }), 404


    db.session.delete(session)

    db.session.commit()


    return jsonify({

        'success': True,

        'session_id': session_id,

        'message': 'Session deleted.'

    })