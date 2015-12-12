from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask.ext.moment import Moment

db = MySQL()
login_manager = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "/login"

    # blueprints
    from views.controllers import main_app
    from models.user.views import user_page_app
    from models.reservations.views import reservation_home_page_app
    from models.admin.views import admin_app
    app.register_blueprint(main_app)
    app.register_blueprint(user_page_app)
    app.register_blueprint(reservation_home_page_app)
    app.register_blueprint(admin_app)
    return app
