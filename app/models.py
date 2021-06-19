from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager
def load_user(user_id):
  return User.query.get(int(user_id ))

class User(db.Model):
  __tablename__='users'
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(255))
  content = db.Column(db.String(255))
  category = db.Column(db.String(255))
  datePosted = db.Column(db.String(255))

class Categories(db.Model):
  __tablename__='categories'
  id = db.Column(db.Integer, primary_key = True)
  category = db.Column(db.String(255))

class Comment(db.Model):
  __tablename__='comments'
  id = db.Column(db.Integer, primary_key = True)
  comment = db.Column(db.String(255))

class Role(db.Model):
  __tablename__='roles'
  id = db.Column(db.Integer, primary_key = True)
  role = db.Column(db.String(255))

class Quote:
  '''
  class defining instance arguments for quote
  '''
  def __init__(self, id, author, quote, link):
    self.id = id
    self.author = author
    self.quote = quote
    self.link = link
