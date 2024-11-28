from flask import (
    Blueprint, flash, g, render_template, request
)

from taxi_app.auth import login_required, attribute
from taxi_app.db import get_db

bp = Blueprint('settings', __name__, url_prefix='/settings')


# I HAVEN'T USED STYLING, SO THIS WON'T DO ANYTHING FOR THE WEBPAGES # (apart from displaying the maps)
# the settings are still saved to the database, however

def get_settings(user):
    db = get_db()
    return db.execute("""
       SELECT *
       FROM tblUserSettings
       WHERE user_id = ?""", (user,)).fetchone()


def get_user():
    return g.user[attribute['user_id']]


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db = get_db()
    user = get_user()

    if request.method == 'POST':

        # 0 = unchecked checkbox
        selected_nightmode = 0 if request.form.get('nightmode') is None else 1
        selected_tts = 0 if request.form.get('text_to_speech') is None else 1

        if user != 1:
            db.execute("""
            UPDATE tblUserSettings
            SET nightmode=?, text_to_speech=?
            WHERE user_id=?""", (selected_nightmode, selected_tts, user))
            db.commit()
        else:
            flash("You cannot save any changes if you are using the Guest account.")

    # GET
    user_settings = get_settings(user)

    return render_template('settings/index.html', nm=user_settings[1],
                           tts=user_settings[2])


@bp.route('/change_ui_colours', methods=['GET', 'POST'])
@login_required
def change_ui_colours():
    return render_template('settings/change_ui_colours.html')


@bp.route('/text_colour_one', methods=['GET', 'POST'])
@login_required
def text_colour_one():
    colour_picker('text_colour_1')

    # GET
    user_settings = get_settings(get_user())

    return render_template('settings/text_colour_one.html', db_colour=user_settings[3])


@bp.route('/text_colour_two', methods=['GET', 'POST'])
@login_required
def text_colour_two():
    colour_picker('text_colour_2')

    # GET
    user_settings = get_settings(get_user())

    return render_template('settings/text_colour_two.html', db_colour=user_settings[4])


@bp.route('/background_colour', methods=['GET', 'POST'])
@login_required
def background_colour():
    colour_picker('background_colour')

    # GET
    user_settings = get_settings(get_user())

    return render_template('settings/background_colour.html', db_colour=user_settings[5])


def colour_picker(column_attribute):
    db = get_db()
    user = get_user()

    if request.method == 'POST':

        colour = request.form.get('colour_choice')

        if user != 1:
            db.execute(f"""
                UPDATE tblUserSettings
                SET {column_attribute}=?
                WHERE user_id=?""", (colour, user))
            db.commit()
        else:
             flash("You cannot save any changes if you are using the Guest account.")
