#!/usr/bin/env python
import sys
import os
from app import app, manager, savvy_collection, db, client
from app.Forms.rego import regoForm
from app.Forms.login import loginForm
from app.Forms.recover import recoverForm
from app.Forms.account import employerForm, candidateForm
from app.Forms.viewProfile import viewProfile
from app.Models.User import User
from app.Helpers.FileHelper import FileHelper
from jinja2 import Environment, FileSystemLoader
from werkzeug import secure_filename
from flask import Flask, request, session, g, redirect, url_for, \
                    abort, render_template, flash, jsonify, \
                    send_from_directory
from flask.ext.login import login_user, logout_user, login_required, current_user
from hashlib import md5

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
        user = savvy_collection.find_one({ "username": username })
        if user:
            return User(user)

    return None

###############################################################################
# Supporting function
###############################################################################
@app.errorhandler(404)
def not_found(error):
    return render('404.html', error=404)

def render(page, form=None, error=None):
    if error:
        return render_template(page,
                               user_logged_in = current_user.is_authenticated,
                               user = current_user.get_id()), error
    else:
        return render_template(page,
                               user_logged_in = current_user.is_authenticated,
                               user = current_user.get_id(),
                               form = form)

###############################################################################
# VIEWS/PAGES
###############################################################################
from app.Views import home
from app.Views import test
from app.Views import dpupload
from app.Views import login
from app.Views import logout
from app.Views import rego
from app.Views import account
from app.Views import recover
