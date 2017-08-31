from flask import Flask
from flask_login import LoginManager
from flaskext.mysql import MySQL
import os

#app configure
app = Flask(__name__)

app.secret_key = 'SECRET_KEY'

#login man config
loginManager = LoginManager()
loginManager.init_app(app)

#MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''
mysql.init_app(app)

from . import views