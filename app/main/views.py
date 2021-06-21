from . import main
from flask import render_template
from .requests import get_quotes

@main.route('/')
def index():

  new_quote = get_quotes()
  return render_template('index.html', new_quote = new_quote)

