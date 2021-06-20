import os
class Config:
  '''
  General settings for application
  '''
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:access@localhost/rudimental'
  UPLOADED_PHOTOS_DEST = 'app/static/photos'

    #  email configurations
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
  MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class ProdCofig(Config):
  '''
  Configurations for production environment
  '''
  # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
  # if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
  #   SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://")

  pass

class DevConfig(Config):
  '''
  configurations for development environment
  '''

  DEBUG = True

config_options = {
  'production':ProdCofig,
  'development':DevConfig
}