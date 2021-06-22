from app import forms
from flask.globals import request
from flask_login import login_required
from . import main
from flask import render_template
from .requests import get_quotes
from flask import abort, flash, redirect, url_for
from .. import photos, db
from ..models import Blog, Category, Comment, User
from .forms import CommentForm, BlogForm, UploadPhoto


@main.route('/')
def index():

  new_quote = get_quotes()
  return render_template('index.html', new_quote = new_quote)

@main.route('/addblog', methods=["GET",'POST'])
@login_required
def addblog():
  form = BlogForm()
  if form.validate_on_submit():
    title = form.title.data
    cat = form.category.data
    category_id = cat
    content = form.content.data

    blog = Blog(title = title, category = category_id, content = content)
    db.session.add(blog)
    db.session.commit()

    return redirect(url_for('main.addblogphotos',blogn = blog.blog_id, blog=blog))
  return render_template('addblog.html', form = form)



@main.route('/upload/<blogn>', methods=['GET','POST'])
@login_required
def addblogphotos(blogn):
  form = UploadPhoto()
  if form.validate_on_submit():
    blog = Blog.query.filter_by(blog_id = blogn).first()
    filename = photos.save(request.files['photo'])
    path = f'photos/{filename}'
    blog.photo_path = path
    db.session.commit()
    
    flash('photo saved')

    return redirect(url_for('main.addblog', blog = blog))
  return render_template('addblogphotos.html', form = form)

@main.route('/<userLogged>/<blogn>/comment', methods = ['GET', 'POST'])
@login_required
def addcomment(blogn, userLogged):
  form = CommentForm()
  if form.validate_on_submit():
    comm = form.comment.data
    user = User.query.filter_by(username = userLogged).first()
    
    added_comment = Comment(comment = comm, blog_parent = blogn, added_by = user.user_id )
    db.session.add(added_comment)
    db.session.commit()

    return redirect(url_for('main.view_blog', comment = added_comment))

  comments = Comment.query.filter(Comment.blog_parent.any(Blog.blog_id.in_([1,2,3]))).all()
  return render_template('comments.html', comments = comments, form = form)

@main.route('/blog')
def view_blog():
  blog = Blog.query.order_by().all()

  return render_template('blog.html', blog=blog)


