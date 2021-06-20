from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_uploads import configure_uploads, UploadSet, IMAGES
from flask_login import LoginManager
from flask_wtf import CsrfProtect
from flask_mail import Mail


bootstrap = Bootstrap()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
login_manager = LoginManager()
csrf = CsrfProtect()
mail = Mail()


def create_app(config_name):
  #initializing app
  app = Flask(__name__)

  #creating app configurations
  app.config.from_object(config_options[config_name])

  #inotializing extensions
  bootstrap.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)
  csrf.init_app(app)
  mail.init_app(app)


  #Registering blueprints
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix = '/authencate')

  #configure uploads
  configure_uploads(app, photos)
  return app