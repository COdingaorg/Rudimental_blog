from sqlalchemy.orm import backref, lazyload
from . import db, login_manager
import base64
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# @login_manager.header_loader
# def load_user_from_header(header_val):
#   header_val = header_val.replace('Basic ', '', 1)
#   try:
#     header_val = base64.b64decode(header_val)
#   except TypeError:
#         pass
#   return User.query.filter_by(api_key=header_val).first()

class Blog(db.Model):
  __tablename__='blogs'
  blog_id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(255))
  content = db.Column(db.String(255))
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
  added_by = db.relationship('Comment', backref='user', lazy='dynamic')

class User(UserMixin, db.Model):
  __tablename__='users'
  user_id = db.Column(db.Integer, primary_key = True)
  fname = db.Column(db.String(100))
  lname = db.Column(db.String(100))
  email = db.Column(db.String(100))
  password_hash = db.Column(db.String())
  user_info = db.relationship('Info', backref='user_info', lazy='dynamic')
  user_role = db.relationship('Role', backref='role', lazy='dynamic')
  blog_posted = db.relationship('Blog', backref='blog_posted',lazy='dynamic')
  comments_added = db.Column(db.Integer,db.ForeignKey('comments.comment'))

class Info(db.Model):
  __tablename__='user_info'
  user = db.Column(db.Integer, db.ForeignKey('users.user_id'))
  bio = db.Column(db.String(100))
  profile_photo = db.Column(db.String())

class Role(db.Model):
  __tablename__='roles'
  role_id = db.Column(db.Integer, primary_key = True)
  role = db.Column(db.String(255))
  user = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class Quote:
  '''
  class defining instance arguments for quote
  '''
  def __init__(self, id, author, quote, link):
    self.id = id
    self.author = author
    self.quote = quote
    self.link = link
