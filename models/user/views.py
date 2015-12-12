from flask import Blueprint, render_template, request, json, redirect, session, url_for, request, flash
from marshmallow import *
from flask_restful import *
from models.forms.forms import LoginForm
from pip._vendor.requests import auth
from models.user.userweb import UserWeb
from models.forms.forms import LoginForm, SignUpForm
from flask_login import login_user, logout_user, current_user, login_required
from models.user.user import User

user_page_app = Blueprint('user_page_app', __name__)
userweb = UserWeb()


@user_page_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        user = userweb.login(username, password)
        if user is not None:
            user.is_active = True
            login_user(user, remember=False, force=False, fresh=True)
            flash('You have logged in successfully!')
            return redirect('/')
        else:
            error = "Login Unsuccessful. Please try again."
    return render_template("index/login.html", form=form, error=error)


@user_page_app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_verify = request.form.get('password_verify')
        error = userweb.validate_login_fields(username, email, password, password_verify)
        if error is None:
            (user, user_exists_error) = userweb.signup(username, password, email)
            if user is None:
                error = user_exists_error
            else:
                login_user(user)
                return redirect('/')
    return render_template("index/signup.html", form=form, error=error)


@user_page_app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@user_page_app.route('/')
def user_index():
    render_template("index/user_index.html")
