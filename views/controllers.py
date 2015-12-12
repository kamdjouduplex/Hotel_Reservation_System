from flask import render_template, request, json, Blueprint, url_for
from models.reservations.reservationservice import ReservationService
from models.user.user import User
from flask_login import user_logged_in
from flask.ext.login import current_user
from flask import current_app
from application import db
from datetime import datetime
from datetime import timedelta
from datetime import date

main_app = Blueprint('main_app', __name__)
reservation_service = ReservationService()


@main_app.route('/')
def main():
    today = date.today()
    if current_user.is_authenticated:
        reservations = reservation_service.get_reservations_by_username(current_user)
        if current_user.username[0] == 'C':
            return render_template("index/user_index.html", reservation_list=reservations, today=today, current_user=current_user)
        elif current_user.username[0] == 'M':
            return render_template("admin/admin_index.html", current_user=current_user)
    else:
        return render_template('index/index.html', current_user=current_user)


'''
@current_app.route('/login')
def login():
    return render_template("login.html")


@current_app.route('/signupform')
def signupform():
    return render_template("signup.html")


@current_app.route('/signup', methods=['POST'])
def signup():
    _name = request.form['username']
    _email = request.form['useremail']
    _password = request.form['userpassword']

    # validate fields
    if _name and _email and _password:
        conn = db.connect()
        cursor = conn.cursor()
        return json.dumps({'html': '<span>valid fields</span>'})
    else:
        return json.dumps({'html': '<span>invalid fields</span>'})
'''
