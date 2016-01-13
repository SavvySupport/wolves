#!/usr/bin/env python
import sys
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
            abort, render_template, flash

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

# MongoDB database setting
client = MongoClient()
client = MongoClient('mongodb://thangdo:Fr0th1ng@ds037415.mongolab.com:37415/thangdodb')
db = client['thangdodb']
collection = db['test_collection']

# Manager authentication with LoginManager
# Handle Login with LoginManager
manager = LoginManager()
manager.init_app(app)

@manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# This import here has to be at the bottom of this file
# To avoid circular references
from app import views
