from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

#Config PostgresSQL


#init PostgresSQL

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
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max= 50)])
	password = PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm', message="Passwords do not match.")])
	confirm = PasswordField('Confirm Password')
	
	#DATABASE FOR USER
	#Create cursor  cursor = (database.connection.cursor())
	#execute query ("INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s), (name, username, email, password))
	#commit to db with (database.connect.commit()
	#close connection cursor.close()
	#flash('You are now registered and can log in', 'success') ** this gives success message
	#return redirect(url_for('login')) redirect for login page
	
#User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))
		
		return render_template('register.html')
	return render_template('register.html', form=form)

#User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		#Get form fields
		username= request.form['username']
		password_candidate = request.form['password']
		
		#create cursor
		#cursor = database.connection.cursor()
		
		#Get user by username
		#result = cursor.execute("SELECT * FROM users WHERE username = %s", [username])
		#if result > 0:
			#get stored hash
			#data = cursor.fetchone()
			#password = data['password'] #gets a tuple if cursorclass is established
			
			#compare passwords
			#if sha256_crypt.verify(password_candidate, password):
				#passed
				#session['logged_in'] = True
				#session['username'] = username
				#flash("You are now logged in", "success")
				#return redirect(url_for('home'))
			#else:
				#error = "Invalid Login"
				#return render_template('login.html', error=error)
		#else:
			#error="User not found"
			#return render_template('login.html', error=error)
		
		pass
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
	