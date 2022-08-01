import cloudinary
from flask import Flask
from flask_babelex import Babel
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'AHKKJDGSDYA&^(!@#!@F!@#>_!(@#UFNUAHSDHASD'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:anhtuan222001@localhost/qlchuyenbay?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
login = LoginManager(app=app)
db = SQLAlchemy(app=app)
babel = Babel(app=app)


@babel.localeselector
def get_locale():
    return 'vi'


cloudinary.config(
    cloud_name='dhldfozup',
    api_key='999276666868985',
    api_secret='-tYCFj4eJA0RLBm3zuk1kFwkeG8'
)