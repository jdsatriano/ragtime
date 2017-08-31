from flask import Flask
from flask_login import LoginManager
from flaskext.mysql import MySQL
import os

#app configure
app = Flask(__name__)

app.secret_key = 'qwertyuioplkjhgfdsazxcvbnm'

#login man config
loginManager = LoginManager()
loginManager.init_app(app)

#MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'jdsatch'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Satchabooty30'
app.config['MYSQL_DATABASE_DB'] = 'ragtime'
app.config['MYSQL_DATABASE_HOST'] = 'ragtimedbinstance.ccykdvhkhfyx.us-east-2.rds.amazonaws.com'
mysql.init_app(app)

from . import views