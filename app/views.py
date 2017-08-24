from flask import Flask, render_template, request, flash, make_response, session, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, mysql
from twilio.rest import Client
from multiprocessing import Process
import eventful, time, MySQLdb

<<<<<<< HEAD
api = eventful.API('YOUR_API_KEY')

# Your Account SID from twilio.com/console
account_sid = 'YOUR_SID'
# Your Auth Token from twilio.com/console
auth_token  = 'YOUR_TOKEN'
=======
api = eventful.API('YOUR_KEY')
>>>>>>> f6d5752848c9e087ffaed2f782f0699429135765

# If you need to log in:
# api.login('username', 'password')

db = MySQLdb.connect(host='localhost', user='root', passwd='Satchabooty30', db='ragtime')
cursor = db.cursor()

#main loop to check each users artistlist and send alerts accordingly
def alert():
	client = Client(account_sid, auth_token)

<<<<<<< HEAD
	cursor.execute('SELECT * FROM users')
	rows = cursor.fetchall()

	for row in rows:
		phone = '+1' + row[3]
		lis = json.loads(row[4])
		for artist in lis:
			#api doesn't accept '&' as in Mumord & Sons, so try changing to 'and'
			try:
				artist = artist.replace('&', 'and')
			except:
				x = 1
			try:
				events = api.call('/events/search', location='Houston, TX', date='Today', keywords=artist)
				for event in events['events']['event']:
				    st = event['title'] + ' at ' + event['venue_name'] + ' ' + event['start_time']
				    message = client.messages.create(
						    to=phone, 
						    from_='+18324302281',
						    body=st)
			except:
				x = 1
			print artist

def loop(x):
	while(True):
		time.sleep(86400)
		alert()
=======
# Your Account SID from twilio.com/console
account_sid = ''
# Your Auth Token from twilio.com/console
auth_token  = ''
>>>>>>> f6d5752848c9e087ffaed2f782f0699429135765

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

	#empty artist list
	artistList = []
	artistList = json.dumps(artistList)

	#authenticate user
	connection = mysql.get_db()
	cursor = connection.cursor()
	cursor.execute('INSERT INTO users (username, password, email, phone, artistlist) VALUES (%s, %s, %s, %s, %s)', (username, hashpass, email, phone, artistList))
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
	cursor.execute('SELECT * FROM musicians WHERE artist LIKE %s LIMIT 10', name+'%')
	rows = cursor.fetchall()

	for row in rows:
		name = row[0]
		lis.append(name)

	artists = {'list': lis}
	return jsonify(artists)

@app.route('/addArtist', methods=['POST'])
def addArtist():
	artistName = request.form['artistName']
	name = session['username']

	connection = mysql.get_db()
	cursor = connection.cursor()
	cursor.execute('SELECT artistlist FROM users WHERE username = %s', name)
	row = cursor.fetchone()

	lis = json.loads(row[0])
	lis.append(artistName)
	lis = json.dumps(lis)

	cursor.execute('UPDATE users SET artistlist = %s WHERE username = %s', (lis, name))
	connection.commit()

	return 'ok'

'''
x = 1
p = Process(target=loop, args=(x,))
p.start()'''














