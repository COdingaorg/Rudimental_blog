from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config_options


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
  #initializing app
  app = Flask(__name__)

  #creating app configurations
  app.config.from_object(config_name[config_options])

  #inotializing extensions
  bootstrap.init_app(app)
  db.init_app(app)


  return app