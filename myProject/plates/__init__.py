from flask import Flask
from flask import session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buguser:Heute000@localhost/plates_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # gegen XSS
app.config['SECRET_KEY'] = '1234321'
app.jinja_env.autoescape = True

# Session statt Cookie idk hilft aber net gegen Keylogger
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False # da lokal
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

db = SQLAlchemy(app)
#
from plates import routes