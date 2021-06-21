from app.auth.forms import LoginForm
from flask_login import login_required, login_user, logout_user
from flask import url_for, request, render_template, redirect, flash
from ..models import User
from . import auth

@auth.route('/login')
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email = form.email.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user, form.remember.data)
      return redirect(request.args.get('next') or url_for('main.index'))
    
    flash('Invalid username or password')
    title = 'Login Page'
    return render_template('login.html', title = title)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.index'))
