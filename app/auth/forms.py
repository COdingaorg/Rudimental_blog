from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import Required, Email

class LoginForm(FlaskForm):
  email = StringField('Enter your email address', validators=[Required(), Email()])
  password = PasswordField('password', validators=[Required()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

