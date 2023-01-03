import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "8025e03296464fdba62af451f646ee44"
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
