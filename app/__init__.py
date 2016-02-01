#!/usr/bin/env python
import sys
import os
from flask import Flask

sys.path.append('/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages')
from pymongo import MongoClient
from flask.ext.login import LoginManager

###############################################################################
# Configuration
###############################################################################
# Flask application setting
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DEBUG = True,
    SECRET_KEY = 'a5428f2f2d5e0c25193922b2c50ea0a3',
    USERNAME = 'wolves',
    PASSWORD = 'SavvyWolves'
))
app.config.from_envvar('SAVVY_SETTING', silent=True)
app.config['basedir'] = os.path.abspath(os.path.dirname(__file__))

# MongoDB database setting
client = MongoClient()
client = MongoClient('mongodb://thangdo:Fr0th1ng@ds037395.mongolab.com:37395/savvydb')
db = client['savvydb']
jobs_collection = db['jobs']
savvy_collection = db['savvy']

# Manager authentication with LoginManager
# Handle Login with LoginManager
manager = LoginManager()
manager.init_app(app)
manager.login_view = 'login'

# This import here has to be at the bottom of this file
# To avoid circular references
from app.Views import views
