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
app.config['MYSQL_DATABASE_USER'] = 'b934367f15db1a'
app.config['MYSQL_DATABASE_PASSWORD'] = 'b69d91c6'
app.config['MYSQL_DATABASE_DB'] = 'heroku_17fda0644a3c554'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-05.cleardb.net'
mysql.init_app(app)

from . import views