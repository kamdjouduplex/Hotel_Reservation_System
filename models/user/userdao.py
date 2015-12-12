from models.user.user import User
from application import db


class UserDao:
    def __init__(self):
        pass

    @classmethod
    def get_all_customers(cls, username, passcode):
        user_list = set()
        cur = db.connection.cursor()
        cur.execute("SELECT user_name, password, email FROM Customer WHERE user_name='%s' AND password='%s';" % (username, passcode))
        user_instance = cur.fetchall()
        for val in user_instance:
            user_name = val[0]
            password = val[1]
            email = val[2]
            user_list.add(User(user_name, password, email))
        cur.close()
        return user_list

    @classmethod
    def get_all_managers(cls, username, passcode):
        user_list = set()
        cur = db.connection.cursor()
        cur.execute("SELECT user_name, password FROM Manager WHERE user_name='%s' AND password='%s';" % (username, passcode))
        user_instance = cur.fetchall()
        for val in user_instance:
            user_name = val[0]
            password = val[1]
            user_list.add(User(user_name, password, None))
        cur.close()
        return user_list

    @classmethod
    def add_user(cls, user):
        # query to add user
        cur = db.connection
        cursor = cur.cursor()
        cursor.execute(
            "INSERT INTO Customer (user_name, password, email) VALUES (%s, %s, %s)", (user.username, user.password, user.email))
        cur.commit()
        cursor.close()
        return user

    @classmethod
    def get_current_user(cls, username):
        name = None
        password = None
        email = None
        user_instance = None
        cur = db.connection.cursor()
        if username[0] == 'C':
            cur.execute("SELECT user_name, password, email FROM Customer WHERE user_name='%s';" % username)
            user_instance = cur.fetchall()
            for val in user_instance:
                name = val[0]
                password = val[1]
                email = val[2]
        elif username[0] == 'M':
            cur.execute("SELECT user_name, password FROM Manager WHERE user_name='%s';" % username)
            user_instance = cur.fetchall()
            for val in user_instance:
                name = val[0]
                password = val[1]
                email = None
        cur.close()
        new_user = User(name, password, email)
        if user_instance is None:
            return "Username does not exist"
        else:
            return new_user

    @classmethod
    def check_username(cls, username):
        user_exists = False
        cur = db.connection.cursor()
        cur.execute("SELECT user_name FROM Customer WHERE user_name='%s';" % username)
        user_instance = cur.fetchone()
        cur.close()
        if user_instance is not None:
            user_exists = True
        return user_exists

    @classmethod
    def check_email(cls, email):
        user_exists = False
        cur = db.connection.cursor()
        cur.execute("SELECT email FROM Customer WHERE email='%s';" % email)
        user_instance = cur.fetchone()
        cur.close()
        if user_instance is not None:
            user_exists = True
        return user_exists
