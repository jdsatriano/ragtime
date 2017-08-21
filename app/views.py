from flask import Flask, render_template, request, flash, make_response, session, json
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, mysql
from twilio.rest import Client
from multiprocessing import Process
import eventful

api = eventful.API('YOUR_KEY')

# If you need to log in:
# api.login('username', 'password')



# Your Account SID from twilio.com/console
account_sid = ''
# Your Auth Token from twilio.com/console
auth_token  = ''

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
	phone = request.form['phone']
	hashpass = generate_password_hash(password) #hash password

	#authenticate user
	connection = mysql.get_db()
	cursor = connection.cursor()
	cursor.execute('INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)', (username, hashpass, email, phone))
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

@app.route('/artistLoad', methods=['POST'])
def load():
	lis = []

	name = request.form['name']
	connection = mysql.get_db()
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM musicians WHERE artist LIKE %s', name+'%')
	rows = cursor.fetchall()

	for row in rows:
		name = row[0]
		lis.append(name)

	artists = {'list': lis}
	return artists


def func(x):
	client = Client(account_sid, auth_token)
	events = api.call('/events/search', location='Holmdel, NJ', date='Future', keywords='John Mayer')
	for event in events['events']['event']:
	    #print "%s at %s" % (event['title'], event['venue_name'])
	    #print event['start_time']
	    st = event['title'] + ' at ' + event['venue_name'] + ' ' + event['start_time']
	    message = client.messages.create(
			    to='+12817148070', 
			    from_='+18324302281',
			    body=st)
'''	    
x = 1
p = Process(target=func, args=(x,))
p.start()'''














