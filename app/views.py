from flask import Flask, render_template, request, flash, make_response, session, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, mysql
from twilio.rest import Client
from multiprocessing import Process
import eventful, time, MySQLdb
from datetime import datetime

# Your Account SID from twilio.com/console
account_sid = 'YOUR_SID'
# Your Auth Token from twilio.com/console
auth_token  = 'YOUR_AUTH_TOKEN'

api = eventful.API('YOUR_API_KEY')

#connect to db, this is for use of alerts
db = MySQLdb.connect(host='localhost', user='root', passwd='Satchabooty30', db='ragtime')
cursor = db.cursor()

#main loop to check each users artistlist and send alerts accordingly
def alert():
	client = Client(account_sid, auth_token)
	cursor.execute('SELECT * FROM users')
	rows = cursor.fetchall()

	for row in rows:
		phone = '+1' + row[3]
		loc = row[5]
		lis = json.loads(row[4])

		for artist in lis:
			#api doesn't accept '&' as in Mumord & Sons, so try changing to 'and'
			try:
				artist = artist.replace('&', 'and')
			except:
				#do nothing
				x = 1
			try:
				events = api.call('/events/search', location=loc, date='This Week', keywords=artist)
				for event in events['events']['event']:
					time = str(event['start_time'])
					d, t = time.split(' ')
					t = t[:-3]
					ti = datetime.strptime(t, '%H:%M')
					ti = ti.strftime("%I:%M %p")
					st = event['title'] + ' at ' + event['venue_name'] + '\n' + d + '\n' + ti
					message = client.messages.create(
						    to=phone, 
						    from_='+18324302281',
						    body=st)
					break #just need one
			except:
				#do nothing
				x = 1

def loop(x):
	while(True):
		time.sleep(86400)
		alert()

x = 1
p = Process(target=loop, args=(x,))
p.start()

#ROUTES
#------------------------------------------------------------------------------
@app.route('/')
def index():
	#if user is still signed in
	if 'username' in session:
		name = session['username']

		connection = mysql.get_db()
		cursor = connection.cursor()
		cursor.execute('SELECT artistList FROM users WHERE username = %s', name)
		row = cursor.fetchone()
		lis = lis = json.loads(row[0])
		lis.reverse()

		user = {
		'name': name,
		'lis': lis,
		'len': len(lis)
		}
		return render_template('userHome.html', user=user)

	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login(): 
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
	location = request.form['location']
	hashpass = generate_password_hash(password) #hash password

	#create empty artist list
	artistList = []
	artistList = json.dumps(artistList)

	#authenticate user
	connection = mysql.get_db()
	cursor = connection.cursor()
	cursor.execute('INSERT INTO users (username, password, email, phone, artistlist, location) VALUES (%s, %s, %s, %s, %s, %s)', 
		(username, hashpass, email, phone, artistList, location))
	connection.commit()

	#send welcoming message
	body = """Welcome, """ + username + """. Ragtime is a new way of keeping up-to-date with your favorite musicians.
	All you have to do is search the name of the band/artist you want to follow, add them to your list, and that is it!
	Ragtime will do the rest and alert you when your favorite musicians are coming to """ + location + """. Enjoy!"""
	client = Client(account_sid, auth_token)
	message = client.messages.create(
						    to=phone, 
						    from_='+18324302281',
						    body=body)

	session['username'] = username
	return username

@app.route('/logout', methods=['POST'])
def logout():
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

	return jsonify(lis)

@app.route('/addArtist', methods=['POST'])
def addArtist():
	artistName = request.form['artistName']
	name = session['username']
	if artistName != '':
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
	else:
		return 'empty artist field error'

@app.route('/removeArtist', methods=['POST'])
def remove():
	artistName = request.form['artistName']
	name = session['username']

	connection = mysql.get_db()
	cursor = connection.cursor()
	cursor.execute('SELECT artistlist FROM users WHERE username = %s', name)
	row = cursor.fetchone()

	lis = json.loads(row[0])
	lis.remove(artistName)
	lis = json.dumps(lis)

	cursor.execute('UPDATE users SET artistlist = %s WHERE username = %s', (lis, name))
	connection.commit()

	return 'ok'




