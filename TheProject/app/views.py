#!/usr/bin/env python
import sys
import os
from app import app
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, session, g, redirect, url_for, \
                    abort, render_template, flash

# Define the template directory
tpldir = os.path.dirname(os.path.abspath(__file__))+'/templates/'

# Setup the template enviroment
env = Environment(loader=FileSystemLoader(tpldir), trim_blocks=True)

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
    return render_template('home.html')

@app.route('/test/<x>')
def test(x):
    return x

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/recover')
def recover():
    return render_template('recover.html')
