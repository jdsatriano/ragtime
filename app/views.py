from flask import Flask, render_template, request, flash, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, mysql
from twilio.rest import Client
from multiprocessing import Process
import eventful

api = eventful.API('your_API_key')

# If you need to log in:
# api.login('username', 'password')

events = api.call('/events/search', q='music', l='San Diego')
for event in events['events']['event']:
    print "%s at %s" % (event['title'], event['venue_name'])


# Your Account SID from twilio.com/console
account_sid = 'AC655a3c0b592ec681b459b61996a88729'
# Your Auth Token from twilio.com/console
auth_token  = 'your_API_key'

@app.route('/')
def index():
	#if user is still signed in
	if 'username' in session:
		name = session['username']
		user = {'name': name}
		return render_template('userHome.html', user=user)

	return render_template('index.html')

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
		user = {'name': username}
		return render_template('userHome.html', user=user)
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

	session['username'] = username
	return username

@app.route('/logout', methods=['POST'])
def logout():
	
	client = Client(account_sid, auth_token)
	message = client.messages.create(
		    to='+12817148070', 
		    from_='+18324302281',
		    body='you logged out of ragtime')
	session.pop('username', None)
	return render_template('index.html')



def func(x):
	while True:
		client = Client(account_sid, auth_token)
		message = client.messages.create(
			    to='+12817148070', 
			    from_='+18324302281',
			    body='you logged out of ragtime')

x = 1
#p = Process(target=func, args=(x,))
#p.start()














