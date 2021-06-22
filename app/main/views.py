from os import abort
import re
from flask.globals import request
from flask_login import login_required
from . import main
from flask import render_template
from .requests import get_quotes
from flask import abort, flash, redirect, url_for
from .. import photos, db
from ..models import Blog, Category


@main.route('/')
def index():

  new_quote = get_quotes()
  return render_template('index.html', new_quote = new_quote)

@main.route('/<userLogged>/addblog', methods=["GET",'POST'])
@login_required
def addblog():
  if request.method == 'POST':
    title = request.form.get('title')
    cat = request.form.get('category')
    category = Category.query.filter_by(category = cat).first()
    category_id = category.category_id
    content = request.form.get('content')

    blog = Blog(title = title, category = category_id, content = content)
    db.session.add(blog)
    db.session.commit()

    return redirect(url_for('main.addblogphotos',blogn = blog.blog_id, blog=blog))
  return render_template('blog.html')



@main.route('/upload/<blogn>', methods=['GET','POST'])
@login_required
def addblogphotos(blogn):
  blog = Blog.query.filter_by(blog_id = blogn).first()
  if request.method =='POST' and 'photo' in request.files:
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    blog.photo_path = path
    db.session.commit()
    
    flash('photo saved')

  return render_template('addblogphotos.html', blog = blog)