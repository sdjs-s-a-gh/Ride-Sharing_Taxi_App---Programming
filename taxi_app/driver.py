from flask import (
    Blueprint, render_template, request
)
from geopy.distance import geodesic

from taxi_app.auth import login_required
from taxi_app.db import get_db

bp = Blueprint('driver', __name__, url_prefix='/driver')


# Displays the drivers in a table format
@bp.route('/search', methods=['GET', 'POST'])
@login_required
def driver_search():
    db = get_db()
    drivers = db.execute("""
    SELECT firstname, surname, average_rating, driver_id, latitude, longitude 
    FROM tblDrivers""").fetchall()

    # makes the jinja easier
    drivers_dict = {
        "firstname": 0,
        "surname": 1,
        "average_rating": 2,
        "driver_id": 3,
        "latitude": 4,
        "longitude": 5,
        "distance": 6,
    }

    user_lat = 54.906101
    user_lng = -1.381130

    formatted_driver_list = []
    for driver in drivers:
        driver_stats = (
            driver[0],
            driver[1],
            round(driver[2], 2),
            driver[3],
            driver[4],
            driver[5],
            calculate_distance(user_lat, user_lng, driver[drivers_dict['latitude']],
                                          driver[drivers_dict['longitude']])
                        )
        formatted_driver_list.append(driver_stats)

    # the list will be ordered by distance by default
    formatted_driver_list_distance = sorted(formatted_driver_list, key=lambda x: x[drivers_dict['distance']],
                                            reverse=False)
    formatted_driver_list = formatted_driver_list_distance
    if request.method == "POST":
        print()
        if request.form.get('combo') == 'rating':
            formatted_driver_list = sorted(formatted_driver_list, key=lambda x: x[drivers_dict['average_rating']],
                                           reverse=True)  # sorts by descending (highest to lowest rating)
        else:
            formatted_driver_list = formatted_driver_list_distance

    return render_template('driver/search.html', drivers=formatted_driver_list, dict=drivers_dict)


@bp.route('/driver_profile/<int:driver_id>', methods=['GET', 'POST'])
@login_required
def driver_profile(driver_id):
    db = get_db()
    driver_details = db.execute("""SELECT * FROM tblDrivers WHERE driver_id = ?""", (driver_id,)).fetchone()
    driver_details_dict = {
        "driver_id": driver_details[0],
        "firstname": driver_details[1],
        "surname": driver_details[2],
        "car_manufacturer": driver_details[3],
        "car_model": driver_details[4],
        "rides_completed": driver_details[5],
        "average_rating": driver_details[6]
    }

    reviews = db.execute("""SELECT title, body, username, rating FROM tblUsers, tblReviews WHERE driver_id = ? 
    AND tblUsers.user_id = tblReviews.user_id""", (driver_id,)).fetchall()

    reviews_dict = {
        "title": 0,
        "body": 1,
        "username": 2,
        "rating": 3
    }

    return render_template('driver/profile.html', driver=driver_details_dict,
                           reviews=reviews, dict=reviews_dict)


# Display the drivers onto a Map to see
@bp.route('/driver_locations', methods=['GET'])
@login_required
def display_drivers():
    db = get_db()
    drivers = db.execute("""
    SELECT driver_id, firstname, surname, latitude, longitude, car_manufacturer, car_model 
    FROM tblDrivers""").fetchall()

    # using a dictionary to put into correct format for js
    driver_list = []
    for driver in drivers:
        driver_dict = {
            "driver_id": driver[0],
            "firstname": driver[1],
            "surname": driver[2],
            "latitude": driver[3],
            "longitude": driver[4],
            "car_manufacturer": driver[5],
            "car_model": driver[6],
        }
        driver_list.append(driver_dict)
    return render_template('map/drivers.html', driver_list=driver_list)


def calculate_distance(user_lat, user_lng, driver_lat, driver_lng):
    user = (user_lat, user_lng)
    driver = (driver_lat, driver_lng)
    distance_miles = geodesic(user, driver).miles
    return f"{round(distance_miles, 2)} miles"  # is very precise otherwise
