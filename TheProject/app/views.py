#!/usr/bin/env python
import sys
from app import app
from flask import Flask, request, session, g, redirect, url_for, \
                    abort, render_template, flash

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

@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/test/<x>')
def test(x):
    return x

@app.route('/resgister')
def register():
    return render_template('register.html')
