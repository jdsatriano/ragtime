from flask import Flask
from flaskext.mysql import MySQL

#app configure
app = Flask(__name__)

#MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Satchabooty30'
app.config['MYSQL_DATABASE_DB'] = 'ragtime'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

import views