from flask_wtf import FlaskForm
from wtforms.fields.core import RadioField, StringField
from wtforms.fields.simple import FileField, SubmitField, TextAreaField
from wtforms.validators import Required, Length

class CommentForm(FlaskForm):
  comment = StringField('Your comment')
  submit = SubmitField('comment')

class BlogForm(FlaskForm):
  title = StringField('Title', validators=[Required()])
  category = RadioField('Category', validators=[Required()], choices=[('1','Technology'),('2','Lifestyle'), ('3', 'Journey')])
  content = TextAreaField('Content', validators=[Required(), Length(min=1, max=6000, message='You have exceeded 6000 characters')], description='Add your story')
  submit= SubmitField('Publish')

class UploadPhoto(FlaskForm):
  photo = FileField('Upload Photo', validators=[Required()],description='Upload one at a time')
  submit = SubmitField('upload')