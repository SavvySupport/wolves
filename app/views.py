#!/usr/bin/env python
import sys
import os
from app import app, manager, savvy_collection, db, client
from app.Forms.rego import regoForm
from app.Forms.login import loginForm
from app.Models.user import User
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, session, g, redirect, url_for, \
                    abort, render_template, flash
from flask.ext.login import login_user, logout_user, login_required, current_user

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
        if not user:
            return None
    else:
        return None
    return User(user)

###############################################################################
# Supporting function
###############################################################################
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

def render(page, form=None):
    return render_template(page,
                           user_logged_in = current_user.is_authenticated,
                           user = current_user.get_id(),
                           form = form)

###############################################################################
# VIEWS/PAGES
###############################################################################
@app.route('/')
def home():
    print(current_user.get_id())
    return render('home.html')

@app.route('/test/<x>')
@login_required
def test(x):
    return render('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Case: user is already logged in
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    # Case: user submits form
    form = loginForm(request.form)
    if request.method == 'POST' and form.validate():
        # redirect to appropriate page
        if request.form.get('next') != None and request.form.get('next') != 'None':
            return redirect(request.form.get('next'))
        else:
            return redirect(url_for('home'))

    # Case: user needs to log in
    return render('login.html', form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Case: user is already logged in
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    form = regoForm(request.form)
    if request.method == 'POST' and form.validate():
        # redirect to appropriate page
        return redirect(url_for('home'))

    return render('register.html', form)

@app.route('/profile/<account>')
@login_required
def profile(account): 
    return account

@app.route('/recover', methods=['GET', 'POST'])
def recover():
    # Case: user is already logged in
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    return render('recover.html')
