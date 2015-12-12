import os
from application import create_app
from models.user.user import User
from application import login_manager
from application import db
from flask.ext.moment import Moment
from models.user.userdao import UserDao

user_dao = UserDao()


@login_manager.user_loader
def load_user(username):
    return user_dao.get_current_user(username)

app = create_app('settings')
moment = Moment(app)
port = int(os.environ.get('PORT', 3000))
app.run(port=port, debug=True)
