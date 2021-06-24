from flask_wtf.recaptcha import validators
from sqlalchemy.orm import backref, lazyload
from wtforms.validators import ValidationError
from . import db, login_manager
import base64
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class Blog(db.Model):
  __tablename__='blogs'
  blog_id = db.Column(db.Integer, primary_key = True)
  photo_path = db.Column(db.String())
  title = db.Column(db.String(255))
  content = db.Column(db.String(6000))
  datePosted = db.Column(db.DateTime, default=datetime.utcnow)
  category = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
  comment = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))
  posted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class Category(db.Model):
  __tablename__='categories'
  category_id = db.Column(db.Integer, primary_key = True)
  category = db.Column(db.String(255))
  blog = db.relationship('Blog', backref='blog', lazy='dynamic')

class Comment(db.Model):
  __tablename__='comments'
  comment_id = db.Column(db.Integer, primary_key = True)
  comment = db.Column(db.String(255))
  blog_parent = db.relationship('Blog', backref='blog_parent', lazy='dynamic')
  added_by = db.relationship('User', backref='user', lazy='dynamic')

class User(UserMixin, db.Model):
  __tablename__='users'
  user_id = db.Column(db.Integer, primary_key = True)
  fname = db.Column(db.String(100))
  lname = db.Column(db.String(100))
  username = db.Column(db.String(100))
  email = db.Column(db.String(100))
  password_hash = db.Column(db.String())
  subscribed = db.Column(db.Boolean, default = False)
  user_info = db.Column(db.Integer, db.ForeignKey('user_info.info_id'))
  user_role = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
  blog_posted = db.relationship('Blog', backref='blog_posted',lazy='dynamic')
  comments_added = db.Column(db.Integer,db.ForeignKey('comments.comment_id'))

  def get_id(self):
    return (self.user_id)

  @property
  def password(self):
    raise ValidationError('Password is hidden')

  @password.setter
  def hash_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def make_admin(self):
    self.user_role = 1

  def make_writer(self):
    self.user_role = 2

  def __repr__(self):
    return ('<User %r>' % self.fname)

class Info(db.Model):
  __tablename__='user_info'
  info_id = db.Column(db.Integer, primary_key = True)
  Info_user = db.relationship('User', backref='info_user', lazy = 'dynamic')
  bio = db.Column(db.String(100))
  profile_photo = db.Column(db.String())

class Role(db.Model):
  __tablename__='roles'
  role_id = db.Column(db.Integer, primary_key = True)
  role = db.Column(db.String(255))
  role_user = db.relationship('User', backref='role_user', lazy = 'dynamic')

class MailingList(db.Model):
  __tablename__='emails'
  email_id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String())
  user_in_list = db.Column(db.String(100))

class Quote:
  '''
  class defining instance arguments for quote
  '''
  def __init__(self, id, author, quote, link):
    self.id = id
    self.author = author
    self.quote = quote
    self.link = link
