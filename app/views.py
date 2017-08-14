from flask import Flask, render_template, request, flash, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, mysql

@app.route('/')
def index():
	if 'username' in session:
		name = session['username']
		user = {'name': name}
		return render_template('userHome.html', user=user)

	return render_template('index.html')

@app.route('/user', methods=['POST', 'GET'])
def userHome():
	if request.method == 'GET':
		return render_template('login.html')

	name = request.form['username']
	user = {'name': name}
	return render_template('userHome.html', user=user)

@app.route('/login', methods=['POST', 'GET'])
def login():
	#for users who try to access '/login' by type GET
	if request.method == 'GET':
		return render_template('login.html')

	#retrieve username, pass and email from register form
	username = request.form['username']
	password = request.form['pass']

	
	#check for user login
	connection = mysql.get_db()
	cursor = connection.cursor()
	cursor.execute('SELECT password FROM users WHERE username = %s', username)
	row = cursor.fetchone()
	hashpass = row[0]

	if check_password_hash(hashpass, password):
		session['username'] = username
		return username
	else:
		return 'didnt work'
	
		
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

	return username

