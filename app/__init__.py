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

  #Registering blueprints
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix = '/authencate')

  return app