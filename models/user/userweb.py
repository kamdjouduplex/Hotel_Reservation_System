from userservice import UserService
from flask import render_template, request, Response, json, jsonify, Blueprint
from userservice import UserService
from user import User

user_service = UserService()


class UserWeb:

    def __init__(self):
        pass

    @classmethod
    def login(cls, username, password):
        return user_service.login(username, password)

    @classmethod
    def signup(cls, username, password, email):
        return user_service.register(username, password, email)

    @classmethod
    def validate_login_fields(cls, username, email, password, password_verify):
        return user_service.validate_login_fields(username, email, password, password_verify)
