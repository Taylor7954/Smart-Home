from flask import (
	Flask, render_template, flash,
	redirect, url_for, session, logging,
	request, make_response, g, redirect
	)
# from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, IntegerField, validators
from passlib.hash import sha256_crypt
<<<<<<< HEAD
from app.models import engine, Session, User, Home, Room
from pygeocoder import Geocoder
=======
from app.models import engine, Session, Home, Room, User
>>>>>>> d9dee1233e55f46cd98298067739a4c7498cf9d5
#Flask babel for translation
from flask_babel import Babel, gettext, lazy_gettext
#to import flask_babel do: pip install flask_babel
#next create the .pot file for language localisation
#to create the .pot file run cmd: pipenv run pybabel extract -F babel.cfg -o messages.pot --input-dirs=.
#from there run cmd: pipenv run pybabel init -i messages.pot -d translations -l ja
#this will make the .po file which will house the translation
#I have done the translations and put them in the spare.txt file
#next run cmd: pipenv run pybabel compile -d translations
#this will make the .mo file which is by the code
<<<<<<< HEAD

=======
from pygeocoder import Geocoder
>>>>>>> d9dee1233e55f46cd98298067739a4c7498cf9d5

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

#Setting main language
@babel.localeselector
def get_locale():
	# print(g.lang)
	return g.lang

<<<<<<< HEAD
#Home page
=======
	return 'ja'

>>>>>>> d9dee1233e55f46cd98298067739a4c7498cf9d5
#Config PostgresSQL

#init PostgresSQL

# handle language switch before rendering page
def get_lang(r):
	lang = r.cookies.get('lang')
	if lang is None:
		lang = 'en'
	g.lang = lang

#Home page1
<<<<<<< HEAD
=======
#Home page
>>>>>>> d9dee1233e55f46cd98298067739a4c7498cf9d5
@app.route('/')
def index():
	get_lang(request)

	return render_template('index.html')

@app.route('/en')
def en():

	get_lang(request)
	g.lang = 'en'

	resp = make_response(render_template('index.html'))
	resp.set_cookie('lang', 'en')
	
	return resp

@app.route('/ja')
def ja():

	get_lang(request)
	g.lang = 'ja'

	resp = make_response(render_template('index.html'))
	resp.set_cookie('lang', 'ja')
	
	return resp
	
#Help page if needed
@app.route('/help')
def help():

	get_lang(request)

	return render_template('help.html')
	
#Group Info
@app.route('/contact')
def contact():

	get_lang(request)

	return render_template('contact.html')

class RegisterForm(Form):
	name = StringField(lazy_gettext('Name'), [validators.Length(min=1, max=50)])
	email = StringField(lazy_gettext('Email'), [validators.Length(min=6, max= 50)])
	address = StringField(lazy_gettext('Address'), [validators.Length(min=6, max= 50)])
	city = StringField(lazy_gettext('City'), [validators.Length(min=6, max= 50)])
	state = StringField(lazy_gettext('State'), [validators.Length(min=6, max= 50)])
	zip = IntegerField(lazy_gettext('Zip Code'))
	password = PasswordField(lazy_gettext('Password'),[
		validators.DataRequired(),
		validators.EqualTo('confirm', message=lazy_gettext("Passwords do not match."))])
	confirm = PasswordField(lazy_gettext('Confirm Password')),


@app.route('/addRoom', methods=['GET', 'POST'])
def addRoom():
	#generate data from input forms
	form = RegisterForm(request.form)
	
	if request.method == 'POST':
		#store form data
		name = form.name.data
		
		#create new db session
		sess = Session()
		
		#get house id for database relations
		home_id = session['home_id']
		
		#create new room: A new home is identified by a name
		new_room = Room(home_id= home_id, name=name)
	
		#Does the Room already exist
		match = sess.query(Room.name)\
        .filter(Room.name==name)\
        .all()
		
		#If the room name is unique the room is added
		if not match:
			print(f'Added: {new_room}')
			#add entry to database for room
			sess.add(new_room)
			
			#save changes
			sess.commit()
			
		#the room name is not unique
		else:
			#error message
			flash("Room name already registered. Please select another name")
			
			#return to register page
			return render_template('registerHouse.html', form=form)
		
		#close connection
		sess.close()
		
		#return to dashboard
		return redirect(url_for('dashboard'))
	return render_template('registerHouse.html', form=form)
	
@app.route('/registerHouse', methods=['GET', 'POST'])
def registerHouse():
	#generate form data

	get_lang(request)

	form = RegisterForm(request.form)
	
	if request.method == 'POST':
		#store form data
		address = form.address.data
		city = form.city.data
		state = form.state.data
		zip = form.zip.data
		
		#generate lat/long from address
		results = Geocoder.geocode(address)
		result = results[0].coordinates
		lat = result[0]
		long = result[1]
		
		#create new db session
		sess = Session()
		
		#get user id for database relations
		account_id=session['id']
		
		#create new home: A new home is identified by street. city, zip, state, lat/long
		new_home = Home(account_id= account_id, street_address=address, city=city, state=state, zip_code=zip, latitude=lat, longitude=long)
	
		#Does the address already exist
		match = sess.query(Home.street_address)\
        .filter(Home.street_address==address)\
        .all()
		
		#If the address is unique the home is added
		if not match:
			print(f'Added: {new_home}')
			#add entry to database for home
			sess.add(new_home)
			
			#save changes
			sess.commit()
			
		#the address is not unique
		else:
			#error message
			flash("Address already registered")
			
			#return to registration page
			return render_template('registerHouse.html', form=form)
		
		#close connection
		sess.close()
		return redirect(url_for('dashboard'))
	return render_template('registerHouse.html', form=form)
	
#User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	#generate form data

	get_lang(request)

	form = RegisterForm(request.form)
	
	if request.method == 'POST':
		#store form data
		name = form.name.data
		email = form.email.data
		password = form.password.data
		
		#create new db session
		session = Session()
		#create new user: A new user is identified by name, email, password
		new_user = User(name=name, email=email, password_hash=password)
	
		#Does the email already exist
		match = session.query(User.email)\
        .filter(User.email==email)\
        .all()
		
		#If the email is unique the user is added
		if not match:
			print(f'Added: {new_user}')
			#add the user to the database
			session.add(new_user)
			#save changes
			session.commit()
		#the email is taken
		else:
			flash(gettext("Email already registered"))
			return render_template('register.html', form=form)
		
		#close connection
		session.close()
		flash(gettext('You are now registered and can log in'), 'success')
<<<<<<< HEAD

=======
		
		#go to login page
>>>>>>> d9dee1233e55f46cd98298067739a4c7498cf9d5
		return redirect(url_for('login'))
		
	#return to registration page
	return render_template('register.html', form=form)

#User Login
@app.route('/login', methods=['GET', 'POST'])
def login():

	get_lang(request)

	if request.method == 'POST':
		#Get form fields
		email= request.form['email']
		password_candidate = request.form['password']
		
		#create db session
		sess = Session()
		
		#Query database for email and password
		userMatch = sess.query(User.email)\
        .filter(User.email==email)\
		.filter(User.password_hash==password_candidate)\
        .all()
	
		name = sess.query(User.name).filter(User.email==email).first()
		id = sess.query(User.id).filter(User.email==email).first()
		
		#If the user and password match
		if userMatch:
			#save session data
			session['logged_in'] = True
			session['id'] = id
			session['name'] = name[0]
			session['id'] = id
			
			flash(gettext("You are now logged in"), gettext("success"))
			return redirect(url_for('index'))
			
		#No entry for user/password pair
		else:
			error=gettext("Invalid Login")
			return render_template('login.html', error=error)
			
	#return to login page
	return render_template('login.html')

#Dashboard
@app.route('/dashboard')
def dashboard():

	#create db session
	sess = Session()
	
	#get user id
	id = session['id']
	
	#Search for entry for house with user id
	match = sess.query(Home.account_id)\
	.filter(Home.account_id==id)\
	.all()
	
	#store data entries
	lat = sess.query(Home.latitude).filter(Home.account_id==id).first()
	long = sess.query(Home.longitude).filter(Home.account_id==id).first()
	address = sess.query(Home.street_address).filter(Home.account_id==id).first()
	id = sess.query(Home.id).filter(Home.account_id==id).first()
	
	#The user has a house
	if match:
		session['has_home'] = True
		if session['has_home']:
			#store session data
			session['latitude'] = lat[0]
			session['longitude'] = long[0]
			session['address'] = address
			session['home_id'] = id
			
	#The user does not have a house registered
	else:
		session['has_home'] = False
		
	#close session
	sess.close()
	
	#Directs to dashboard
	
	get_lang(request)

	return render_template('dashboard.html')

#log out
@app.route('/logout')
def logout():
	#clears session data on logout

	get_lang(request)

	session.clear()
<<<<<<< HEAD
	flash(gettext('You are now logged out'), gettext('success'))
=======
	flash(gettext('You are now logged out'), 'success')
>>>>>>> d9dee1233e55f46cd98298067739a4c7498cf9d5
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)
	