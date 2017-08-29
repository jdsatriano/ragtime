from flask import Flask
from flask_login import LoginManager
from flaskext.mysql import MySQL
import os

#app configure
app = Flask(__name__)

app.secret_key = os.urandom(24)

#login man config
loginManager = LoginManager()
loginManager.init_app(app)

#MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'b69d91c6'
app.config['MYSQL_DATABASE_DB'] = 'ragtime'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

from . import views