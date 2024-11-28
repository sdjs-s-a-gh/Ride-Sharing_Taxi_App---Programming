from flask import (
    Blueprint, redirect, render_template, request, url_for, flash, g
)

from taxi_app.auth import login_required, attribute
from taxi_app.db import get_db

bp = Blueprint('book_a_ride', __name__, url_prefix='/book_a_ride')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db = get_db()
    driver_id = request.args.get('driver_id', get_driver_id())  # gets the driver_id from the url parameter
                                                # as the user could have went back onto that page from somewhere else
    full_address = get_collection_address()
    name = get_driver_name()
    destination_add = get_destination()
    if driver_id is not None:
        db_name = db.execute("SELECT firstname, surname FROM tblDrivers WHERE driver_id = ?", (driver_id,)).fetchone()
        name = f"{db_name[0]} {db_name[1]}"
        set_driver_name(name)
        set_driver_id(driver_id)    # so the user can go back to this page without the id changing back to None

    if request.method == "POST":
        print(request.form.get('submit'))
        if request.form.get('submit') == "clear":
            print("this is working")
            set_destination(None)  # reset both addresses
            set_collection_address(None)
            set_driver_id(None)
            set_driver_name(None)
            return redirect(url_for('book_a_ride.index'))
        if not get_destination() or not get_collection_address() or not get_driver_id():
            flash("You must enter all three fields of information.")
        elif get_destination() == get_collection_address():
            flash("The collection and destination addresses must be different.")
            set_destination(None)       # reset both addresses
            set_collection_address(None)
        else:
            return redirect(url_for('book_a_ride.current_ride'))

    return render_template('book_a_ride/index.html', name=name, full_address=full_address,
                           destination_add=destination_add)


@bp.route('/collection_point', methods=['GET', 'POST'])
@login_required
def collection_point():
    # input handling is done in the html file (js)

    if request.method == 'POST':
        data = request.get_json()
        set_collection_address(data.get('full_address', None))
        set_collection_coordinates(data.get('coordinates', None))
        return redirect(url_for('book_a_ride.index'))

    return render_template('book_a_ride/collection_point.html')


@bp.route('/destination', methods=['GET', 'POST'])
@login_required
def destination():
    # input handling is done in the html file (js)

    if request.method == 'POST':
        data = request.get_json()
        set_destination(data.get('full_address', None))
        set_destination_coordinates(data.get('coordinates', None))
        print(destination)
        return redirect(url_for('book_a_ride.index'))

    return render_template('book_a_ride/destination.html')


@bp.route('/current_ride', methods=['GET', 'POST'])
@login_required
def current_ride():
    collection_address = get_collection_coordinates().split(",", 1)
    formatted_collection_address = {
        "latitude": float(collection_address[0]),
        "longitude": float(collection_address[1])
    }
    destination_address = get_destination_coordinates().split(",", 1)
    formatted_destination_address = {
        "latitude": float(destination_address[0]),
        "longitude": float(destination_address[1])
    }

    return render_template('map/ride_routes.html', collection_coordinates=formatted_collection_address,
                           destination_coordinates=formatted_destination_address)


@bp.route('/end_of_ride', methods=['GET', 'POST'])
@login_required
def end_of_ride():
    db = get_db()
    if request.method == "POST":
        rating = request.form.get('combo')
        title = request.form.get('title')
        body = request.form.get('body')
        user_id = g.user[attribute['user_id']]
        driver_id = get_driver_id()

        cursor = db.cursor()    # cursor has to be the exact same to get the 'lastrowid' (db.cursor() does not work)
        cursor.execute("INSERT INTO tblReviews (user_id, title, body, rating, driver_id) VALUES (?, ?, ?, ?, ?)",
                   (user_id, title, body, rating, driver_id))

        review_id = cursor.lastrowid    # review_id is auto-incremented, so this function will return that value

        db.execute("INSERT INTO tblRides (user_id, driver_id, review_id) VALUES (?, ?, ?)",
                       (user_id, driver_id, review_id))

        # update other tables to ensure statistics are correct
        average_rating = db.execute("SELECT COALESCE(AVG(rating), 0) FROM tblReviews WHERE driver_id = ?",
                                    (driver_id,)).fetchone()[0]
        rides_completed = db.execute("SELECT COALESCE(COUNT(rating), 0) FROM tblReviews WHERE driver_id = ?",
                                     (driver_id,)).fetchone()[0]

        db.execute("UPDATE tblDrivers SET average_rating = ?, rides_completed = ? WHERE driver_id = ?",
                   (average_rating, rides_completed, driver_id))

        db.commit()
        return redirect(url_for('home.index'))

    return render_template('book_a_ride/end_of_ride.html')


# if the values have not been defined yet (which most of them aren't when going onto the pages for the first time),
# None is returned
def set_driver_id(drv_id):
    global driver_id_selected
    driver_id_selected = drv_id


def get_driver_id():
    try:
        driver_id_selected
    except NameError:
        return None
    else:
        return driver_id_selected


def set_driver_name(name):
    global driver_name_selected
    driver_name_selected = name


def get_driver_name():
    try:
        driver_name_selected
    except NameError:
        return None
    else:
        return driver_name_selected


def set_collection_address(address):
    global collection_point_address
    collection_point_address = address


def get_collection_address():
    try:
        collection_point_address
    except NameError:
        return None
    else:
        return collection_point_address


def set_collection_coordinates(coordinates):
    global collection_point_coordinates
    collection_point_coordinates = coordinates


def get_collection_coordinates():
    try:
        collection_point_coordinates
    except NameError:
        return None
    else:
        return collection_point_coordinates

def set_destination_coordinates(coordinates):
    global destination_coordinates
    destination_coordinates = coordinates


def get_destination_coordinates():
    try:
        destination_coordinates
    except NameError:
        return None
    else:
        return destination_coordinates


def set_destination(address):
    global destination_address
    destination_address = address


def get_destination():
    try:
        destination_address
    except NameError:
        return None
    else:
        return destination_address

