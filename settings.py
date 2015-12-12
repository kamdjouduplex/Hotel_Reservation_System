import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
PROJECT_SITE_URL = u'http://127.0.0.1:3000/'
WTF_CSRF_ENABLED = True
PORT = 3000

SECRET_KEY = 'blah-blah'


# MYSQL SETTINGS
MYSQL_USER = 'reservation_user'
MYSQL_PASSWORD = 'password'
MYSQL_DB = 'reservation_db'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
