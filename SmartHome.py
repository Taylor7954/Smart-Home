from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
# from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, IntegerField, validators
from passlib.hash import sha256_crypt
from app.models import engine, Session, User

app = Flask(__name__)

#Home page
@app.route('/')
def index():
	return render_template('index.html')
	
#Help page if needed
@app.route('/help')
def help():
	return render_template('help.html')
	
#Group Info
@app.route('/contact')
def contact():
	return render_template('contact.html')

class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	email = StringField('Email', [validators.Length(min=6, max= 50)])
	address = StringField('Address', [validators.Length(min=6, max= 50)])
	city = StringField('City', [validators.Length(min=6, max= 50)])
	state = StringField('State', [validators.Length(min=6, max= 50)])
	zip = IntegerField('Zip Code')
	password = PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm', message="Passwords do not match.")])
	confirm = PasswordField('Confirm Password')

@app.route('/registerHouse', methods=['GET', 'POST'])
def registerHouse():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		address = form.address.data
		city = form.city.data
		state = form.state.data
		zip = form.zip.data
		
		return render_template('registerHouse.html')
	return render_template('registerHouse.html', form=form)
	
#User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST':
		name = form.name.data
		email = form.email.data
		password = form.password.data
		
		#create new db session
		session = Session()
		#create new user: A new user is identified by name, email, password
		new_user = User(name=name, email=email, password_hash=password)
	
		#Does the email already exist
		###match = session.query(User).filter(User.email==email)

		match = session.query(User.email)\
        .filter(User.email==email)\
        .all()
		#If the email is unique the user is added
		if not match:
			print(f'Added: {new_user}')
			session.add(new_user)
			#save changes
			session.commit()
		else:
			flash("Email already registered")
			return render_template('register.html', form=form)
		
		#close connection
		session.close()
		flash('You are now registered and can log in', 'success')
		
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

#User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		#Get form fields
		email= request.form['email']
		password_candidate = request.form['password']
		
		sess = Session()
		
		#Query database for email and password
		userMatch = sess.query(User.email)\
        .filter(User.email==email)\
		.filter(User.password_hash==password_candidate)\
        .all()
		
		name = sess.query(User.name).filter(User.email==email).first()
		
		if userMatch:
			session['logged_in'] = True
			session['name'] = name[0]
			flash("You are now logged in", "success")
			return redirect(url_for('index'))
		else:
			error="Invalid Login"
			return render_template('login.html', error=error)
	return render_template('login.html')

#Dashboard
@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

#log out
@app.route('/logout')
def logout():
	session.clear()
	flash('You are now logged out', 'success')
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)
	