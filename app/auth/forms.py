from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import EqualTo, Required, Email, ValidationError
from ..models import User

class LoginForm(FlaskForm):
  email = StringField('Enter your email address', validators=[Required(), Email()])
  password = PasswordField('password', validators=[Required()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class RegisterForm(FlaskForm):
  fname = StringField('First Name: ', validators=[Required()])
  lname = StringField('Last Name: ', validators=[Required()])
  email = StringField('email address', validators=[Required(), Email()])
  password = PasswordField('Enter password', validators=[Required(), EqualTo('confirm_password', message = 'password must be the same')])
  confirm_password = PasswordField('Confirm password', validators=[Required()])
  submit = SubmitField('sign up')

  def validate_email(self, data_field):
    if User.query.filter_by(email= data_field.data).first():
      raise ValidationError('Email address already taken', 'error')

