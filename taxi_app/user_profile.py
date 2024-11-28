import re
import datetime
from flask import (
    Blueprint, flash, g, render_template, request
)

from taxi_app.auth import login_required, attribute
from taxi_app.db import get_db

bp = Blueprint('user_profile', __name__, url_prefix='/user_profile')


def get_settings(user):
    db = get_db()
    return db.execute("""
       SELECT *
       FROM tblUserSettings
       WHERE user_id = ?""", (user,)).fetchone()


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user = g.user[attribute['username']]
    return render_template('user_profile/index.html', username=user)


@bp.route('/manage_account', methods=['GET', 'POST'])
@login_required
def manage_account():
    db = get_db()
    user_id = g.user[attribute['user_id']]

    if request.method == 'POST':
        username = request.form.get('new_username')
        password = request.form.get('new_password')
        email = request.form.get('new_email')

        error = None

        if user_id != 1:

            if len(username) + len(password) + len(email) == 0:
                error = "You have not selected to change anything."
            elif len(email) > 0 and not re.match("^[\w\.-]+@[\w\.-]+\.com$", email):
                error = "Email is invalid. MUST contain an '@' and finish with the '.com' domain name."

            if error is None:
                try:
                    if len(username) > 0:
                        # without querying, allows me to duplicate usernames somehow
                        existing_user = db.execute(
                            "SELECT * FROM tblUsers WHERE username = ?",
                            (username,)
                        ).fetchone()
                        if existing_user is not None:
                            error = "Username already exists."
                        else:
                            db.execute(
                                "UPDATE tblUsers SET username=? WHERE user_id=?",
                                (username, user_id)
                            )
                    if len(password) > 0:
                        db.execute(
                            "UPDATE tblUsers SET password=? WHERE user_id=?",
                            (password, user_id)
                        )
                    if len(email) > 0:
                        db.execute(
                            "UPDATE tblUsers SET email=? WHERE user_id=?",
                            (email, user_id)
                        )
                    db.commit()
                except Exception as x:
                    error = x
                if error is None:
                    flash("Your credentials have been successfully changed.")
            if error is not None:
                flash(error)
        else:
            flash("You cannot save any changes if you are using the Guest account.")

    return render_template('user_profile/manage_account.html')


@bp.route('/view_booking_history', methods=['GET', 'POST'])
@login_required
def view_booking_history():
    db = get_db()
    user = g.user[attribute['user_id']]

    booking_history = db.execute("""
    SELECT tblRides.driver_id, tblDrivers.firstname, tblDrivers.surname, tblRides.Date, tblReviews.rating
    FROM tblRides, tblReviews, tblDrivers
    WHERE tblRides.user_id = ? AND tblReviews.user_id = ? AND tblRides.driver_id = tblReviews.driver_id 
    AND tblRides.driver_id = tblDrivers.driver_id""", (user, user)). fetchall()
    print(booking_history)
    # changing the date format
    formatted_booking_history = []
    column_attribute = {
        'driver_id': 0,
        'firstname': 1,
        'surname': 2,
        'date': 3,
        'rating': 4
    }
    if booking_history is not None:
        for row in booking_history:
            new_row = (
                row[column_attribute['driver_id']],
                row[column_attribute['firstname']],
                row[column_attribute['surname']],
                datetime.datetime.strptime(row[column_attribute['date']], '%Y-%m-%d %H:%M:%S').
                strftime('%d/%m/%Y %H:%M'),
                row[column_attribute['rating']]
            )
            formatted_booking_history.append(new_row)
            print(new_row)
        booking_history = formatted_booking_history

    return render_template('user_profile/view_booking_history.html', booking_history=booking_history,
                           dict=column_attribute)


@bp.route('/reviews', methods=['GET', 'POST'])
@login_required
def reviews():
    db = get_db()
    user = g.user[attribute['user_id']]

    reviews = db.execute("""
    SELECT title, body, firstname, surname, rating
    FROM tblReviews, tblDrivers
    WHERE tblReviews.user_id = ? AND tblReviews.driver_id = tblDrivers.driver_id""", (user,)).fetchall()

    reviews_attributes = {
        "title": 0,
        "body": 1,
        "firstname": 2,
        "surname": 3,
        "rating": 4
    }
    return render_template('user_profile/reviews.html', reviews=reviews, dict=reviews_attributes)
