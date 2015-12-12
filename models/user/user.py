from flask import Flask, json
from flask import current_app
import hashlib
import uuid


class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_email(self):
        return self.email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)
