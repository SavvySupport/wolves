#!/usr/bin/env python
import sys
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
            abort, render_template, flash

sys.path.append('/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages')
import pymongo
from pymongo import MongoClient
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

###############################################################################
# Supporting function
###############################################################################
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

###############################################################################
# VIEWS/PAGES
###############################################################################
@app.route('/')
def home():
    return "Home Page"

@app.route('/index')
def index():
    return "hello world!!"
