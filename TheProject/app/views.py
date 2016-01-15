#!/usr/bin/env python
import sys
import os
from app import app, manager, collection, db, client
from .Models.user import User
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
    user = collection.find_one({ "username": username })
    if not user:
        return None
    return User(user)

###############################################################################
# Supporting function
###############################################################################
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

def render(page):
    return render_template(page,
                           user_logged_in = current_user.is_authenticated,
                           user = current_user.get_id())

###############################################################################
# VIEWS/PAGES
###############################################################################
@app.route('/')
def home():
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
    if request.method == 'POST':
        # Query from database and perform validation
        user = collection.find_one({ "username": request.form['username'] })

        # if user and (user['password'] == request.form['password']):
        if user and User.validate_login(request.form['password'], user['password']):
            userObj = User(user['username'])
            login_user(userObj)

            # redirect to appropriate page
            if request.form.get('next') != None and request.form.get('next') != 'None':
                return redirect(request.form.get('next'))
            else:
                return redirect(url_for('home'))
        else:
            flash(u'Incorrect login credentials', 'error')

    # Case: user needs to log in
    return render('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Case: user is already logged in
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        user = {
            "username": request.form['username'],
            "password": request.form['password'],
            "email"   : request.form['email'] }

        try:
            collection.insert(user)
            # flash('You are successfully logged in')
        except:
            # flash('Failed to log in')
            pass

        # return "<h2>ASDAD</h2>"
        # userObj = User(user)
        # login_user(userObj)
        #
        # # redirect to appropriate page
        # if request.form.get('next') != None:
        #     return redirect(request.form.get('next'))
        # else:
        #     return redirect(url_for('home'))

    return render('register.html')

@app.route('/recover', methods=['GET', 'POST'])
def recover():
    # Case: user is already logged in
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    return render('recover.html')
