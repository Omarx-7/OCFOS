#Turn app/website into a python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

#Initialise extensions
db = SQLAlchemy()

def ocfapp():
    app = Flask(__name__)

    #Load DB configuration settings config.py
    app.config.from_object(Config) #'Config' arg being the class imported from config.py

    #Bind Initialised Extensions
    db.init_app(app) #Bind SQLAlchemy to app after initialising it

    #import and register blueprints - this ensures that flask can access routes
    from .views import views

    app.register_blueprint(views, url_prefix='/' )  #By importing&registering vies, these route blueprints become available to Flask.

    return app