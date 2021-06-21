from app.auth.forms import LoginForm, RegisterForm
from flask_login import login_required, login_user, logout_user
from flask import url_for, request, render_template, redirect, flash
from ..models import User, generate_password_hash
from . import auth
from .. import db
from ..main.mail import mail_message
from random import randint
@auth.route('/login', methods= ['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email = form.email.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user, form.remember.data)
      return redirect(request.args.get('next') or url_for('main.index'))
    
    flash('Invalid username or password')
  title = 'Login Page'
  return render_template('auth/login.html', title = title, form = form)

@auth.route('/logout', methods= ['GET', 'POST'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    lister = list(form.fname.data)
    aNum = randint(0, 2021)
    
    user = User(fname = form.fname.data, user_role = 1, lname = form.lname.data, username = (form.lname.data)+(lister[0])+str(aNum), email = form.email.data, password_hash = generate_password_hash(form.password.data) )
    db.session.add(user)
    db.session.commit()
 
    mail_message('Welcome to Redimental Blog', 'email/welcome', user.email, user=user)

    return redirect(url_for('auth.login'))
  title = 'Create Account'
  return render_template('auth/register.html', form = form, title = title)