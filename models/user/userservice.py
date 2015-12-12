import uuid
from userdao import UserDao
from user import User
from random import randint

user_dao = UserDao()


class UserService:

    def __init__(self):
        pass

    @classmethod
    def login(cls, username, password):
        users = None
        if username[0] == 'C':
            users = user_dao.get_all_customers(username, password)
        elif username[0] == 'M':
            users = user_dao.get_all_managers(username, password)
        if users is not None:
            for user in users:
                if user.get_username() == username and user.get_password() == password:
                    return user
        return None

    @classmethod
    def register(cls, username, password, email):
        # ensure this user hasn't already registered
        error = None
        new_user = None
        if cls.check_email(email) is True:
            error = "The email address provided is already associated with another account"
        elif cls.check_username(username) is True:
            error = "The username provided is already associated with another account"
        else:
            new_user = User(str(username), str(password), str(email))
            user_dao.add_user(new_user)
        return new_user, error

    @classmethod
    def check_username(cls, username):
        return user_dao.check_username(username)

    @classmethod
    def check_email(cls, email):
        return user_dao.check_email(email)

    @classmethod
    def get_all_users(cls):
        user_list = []
        user_list = user_dao.get_all_customers()

    @classmethod
    def validate_login_fields(cls, username, email, password, password_verify):
        error = None
        if email == '' or password == '' or password_verify == '':
            error = "All fields must be completed"
        elif username[0] != 'C':
            error = "Username must begin with the letter C"
        elif not username[1:len(username)].isdigit():
            error = "Username must be in the format C######..."
        elif password != password_verify:
                error = "Passwords do not match"
        return error



