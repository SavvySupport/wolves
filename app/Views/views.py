#!/usr/bin/env python

import os
from app import app, savvy_collection, manager
from jinja2 import Environment, FileSystemLoader
from flask import render_template
from flask.ext.login import current_user
from app.Models.User import User
from app.Helpers.Constant import *

###############################################################################
# Set up environment for Jinja
###############################################################################
# Define the template directory
tpldir = os.path.dirname(os.path.abspath(__file__))+'/templates/'

# Setup the template enviroment
env = Environment(loader=FileSystemLoader(tpldir), trim_blocks=True)

###############################################################################
# Login Manager
###############################################################################
@manager.user_loader
def load_user(username):
    if username != None:
        user = savvy_collection.find_one({ USERNAME: username })
        if user:
            return User(user)

    return None

###############################################################################
# Supporting function
###############################################################################
@app.errorhandler(404)
def not_found(error):
    return render('404.html', error=404)

def render(page, form=None, error=None, jsonObject=None, extra=None):
    if error:
        return render_template(page,
                               user_logged_in = current_user.is_authenticated,
                               user = current_user.get_id()), error
    else:
        return render_template(page,
                               user_logged_in = current_user.is_authenticated,
                               user = current_user.get_id(),
                               form = form,
                               jsonObject = jsonObject,
                               extra = extra)

###############################################################################
# VIEWS/PAGES
###############################################################################
from app.Views import home
from app.Views import test
from app.Views import dpupload
from app.Views import connect
from app.Views import login
from app.Views import logout
from app.Views import rego
from app.Views import account
from app.Views import recover
from app.Views import jobs
from app.Views import search
