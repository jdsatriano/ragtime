from flask import Flask
from flask_login import LoginManager
from flaskext.mysql import MySQL

#app configure
app = Flask(__name__)

#login man config
loginManager = LoginManager()
loginManager.init_app(app)

#MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Satchabooty30'
app.config['MYSQL_DATABASE_DB'] = 'ragtime'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

import views