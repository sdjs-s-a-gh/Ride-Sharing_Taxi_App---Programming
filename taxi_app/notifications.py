from flask import (
    Blueprint, flash, g, render_template, request
)

from taxi_app.auth import login_required, attribute
from taxi_app.db import get_db

bp = Blueprint('notifications', __name__, url_prefix='/notifications')


def get_settings(user):
    db = get_db()
    return db.execute("""
       SELECT *
       FROM tblUserNotificationSettings
       WHERE user_id = ?""", (user,)).fetchone()


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db = get_db()
    user = g.user[attribute['user_id']]

    if request.method == 'POST':

        # 0 = unchecked checkbox
        push_notifications = 0 if request.form.get('push_notifications') is None else 1
        enroute_driver_updates = 0 if request.form.get('driver_updates') is None else 1
        special_offers = 0 if request.form.get('special_offers') is None else 1
        booking_receipts = 0 if request.form.get('booking_receipts') is None else 1

        if user != 1:
            db.execute("""
            UPDATE tblUserNotificationSettings
            SET push_notifications=?, enroute_driver_updates=?, special_offers=?, booking_receipts=?
            WHERE user_id=?""",
                       (push_notifications, enroute_driver_updates, special_offers, booking_receipts, user))
            db.commit()
        else:
            flash("You cannot save any changes if you are using the Guest account.")

    # GET
    notification_settings = get_settings(user)

    return render_template('notifications/index.html', notif=notification_settings[1],
                           enr=notification_settings[2], spo=notification_settings[5],
                           bkr=notification_settings[6])


@bp.route('/distance', methods=['GET', 'POST'])
@login_required
def distance():
    db = get_db()
    user = g.user[attribute['user_id']]
    distance_options = {
        "one_mile": 1,
        "two_miles": 2,
        "three_miles": 3
    }

    if request.method == 'POST':

        choice = request.form.get('distance')
        selected_distance = distance_options[choice]

        if user != 1:
            db.execute("""
            UPDATE tblUserNotificationSettings
            SET distance=?
            WHERE user_id=?""", (selected_distance, user))
            db.commit()
        else:
            flash("You cannot save any changes if you are using the Guest account.")

    # GET
    notification_settings = get_settings(user)

    return render_template('notifications/distance.html', distance=notification_settings[3])


@bp.route('/time', methods=['GET', 'POST'])
@login_required
def time():
    db = get_db()
    user = g.user[attribute['user_id']]
    time_options = {
        "one_minute": 1,
        "two_minutes": 2,
        "three_minutes": 3,
        "five_minutes": 5
    }

    if request.method == 'POST':

        choice = request.form.get('time')
        selected_time = time_options[choice]

        if user != 1:
            db.execute("""
            UPDATE tblUserNotificationSettings
            SET time=?
            WHERE user_id=?""", (selected_time, user))
            db.commit()
        else:
            flash("You cannot save any changes if you are using the Guest account.")

    # GET
    notification_settings = get_settings(user)

    return render_template('notifications/time.html', minute=notification_settings[4])
