from flask.globals import request
from flask_login import login_required
from . import main
from flask import render_template
from .requests import get_quotes
from flask import abort, flash, redirect, url_for
from .. import photos, db
from ..models import Blog, Category, Comment, MailingList, User
from .forms import CommentForm, BlogForm, UploadPhoto
from ..main.mail import mail_message


@main.route('/')
def index():
  blogList = Blog.query.filter_by(Blog.blog_id).all()
  leng = int(len(blogList))-1
  lengt = int(len(blogList))-2
  blog = blogList[leng]
  blog2 = blogList[lengt]

  new_quote = get_quotes()

  return render_template('index.html', new_quote = new_quote, blog1 = blog, blog2 = blog2, blogList = blogList)


@main.route('/addblog/<userLogged>', methods=["GET",'POST'])
@login_required
def addblog(userLogged):
  form = BlogForm()
  if form.validate_on_submit():
    title = form.title.data
    cat = form.category.data
    category_id = cat
    content = form.content.data

    blog = Blog(title = title, category = category_id, content = content)
    db.session.add(blog)
    db.session.commit()

    email_listset = ['calemasanga@gmail.com']
    email_list = MailingList.query.with_entities(MailingList.email).all()
    for emailt in email_list:
      email_listset.append(emailt)
      return email_listset
    for email in email_listset:
      mail_message('New Post has been made', 'email/newpost', email, user=userLogged)

    return redirect(url_for('main.addblogphotos',blogn = blog.blog_id, blogs=blog))
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

    return redirect(url_for('main.view_blog', blog = blog))
  return render_template('addblogphotos.html', form = form)

@main.route('/<userLog>/<blogn>/comments', methods = ['GET', 'POST'])
@login_required
def addcomment(blogn, userLog):
  form = CommentForm()
  userid = (User.query.filter(User.username == userLog).first()).user_id
  user = Comment.query.get_or_404(userid)
  blog = Blog.query.get_or_404(blogn)
  if form.validate_on_submit():
    comm = form.comment.data
    added_comment = Comment(comment = comm, blog_parent = blog.blog_id, added_by = userid )
    db.session.add(added_comment)
    db.session.commit()
    flash("Your comment has been added to the post", "success")
    comments = Comment.query.filter_by(blog_parent = blog.blog_id).with_entities(Comment.comment).all()

    return redirect(url_for('main.view_blog', comment = added_comment))

  comments = Comment.query.get_or_404(blog.blog_id).all()
  return render_template('main/comments.html', comments = comments, form = form)

@main.route('/blog')
def view_blog():
  blog = Blog.query.order_by().all()

  return render_template('blog.html', blog=blog)

@main.route('/<url_link>')
def view_category(url_link):
  links = ['https://www.cnet.com/','https://www.menshealth.com/technology-gear/','https://www.goodreads.com/quotes/tag/life-journey']
  if url_link == '1':
    url_lin = links[0]
  elif url_link == '2':
    url_lin = links[1]
  else:
    url_lin = links[2]

  return render_template('index.html', url_link = url_lin)

@main.route('/<userLogged>/subscribed')
@login_required
def subscribe(userLogged):
  query1 = User.query.filter(User.username == userLogged).first()
  if query1:
    query1.subscribed = True
    db.session.add(query1)#update({'subscribed':(t)})
    db.session.commit()

    mail_list = MailingList(email = query1.email)
    db.session.add(mail_list)
    db.session.commit()

    #   return redirect(url_for('main.addblog',user = user.subscribed))
  
  
  title = 'Subscribed successfully, Thank you'
  return render_template('subscribed.html', user = 'user.subscribed', title = title)
