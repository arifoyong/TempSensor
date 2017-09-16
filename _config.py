import os

#get the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = "iot.db"
SECRET_KEY = 'secret!'

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
