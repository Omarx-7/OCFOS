#Config settings for Flask app, including db connection details
#Flask uses config settings on startup - where configs are used in __init__.py

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv() #reads the .env file and loads its values into os.environ

#Database config - info needed to connect to the db
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False