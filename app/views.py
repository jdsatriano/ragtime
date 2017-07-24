from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, mysql

@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/login')
def login():
	return render_template('login.html', title='login')

@app.route('/register', methods=['POST'])
def register():
	#retrieve username, pass and email from register form
	username = request.form['username']
	password = request.form['pass']
	email = request.form['email']
	hashpass = generate_password_hash(password) #hash password

	#authenticate user
	connection = mysql.get_db()
	cursor = connection.cursor()
	cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, hashpass, email))
	connection.commit()

	return render_template('index.html', title='register')

