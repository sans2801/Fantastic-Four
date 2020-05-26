from flask import render_template, url_for, flash, redirect, request
from meetify import app,db,bcrypt
from meetify.forms import RegistrationForm, LoginForm, UpdateAccountForm
from meetify.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
	return render_template('HomePage.html')



@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	
	form = LoginForm()	
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user)
			return redirect(url_for('account'))
		else:
			flash('please check your credentials', 'danger')
	return render_template('login.html', form =form)


@app.route('/account')
@login_required
def account():
	form=UpdateAccountForm()
	image_file=url_for('static',filename='profilepics/'+current_user.image_file)
	return render_template('myprofile.html',title='Personal Dashboard',image_file=image_file,form=form)


@app.route('/signup',methods=['GET','POST'])
def signup():	
	form = RegistrationForm()
	
	
	if form.validate_on_submit():
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user1=User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user1)
		db.session.commit()
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	else:
		flash('Please check email and password')
	return render_template('signup.html', form= form)

@app.route('/forgot_password')
def forgot_password():
	return render_template('forgot_password.html')

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))
