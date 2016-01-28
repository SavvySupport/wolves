from app import app, savvy_collection
from app.Views.views import render
from app.Forms.account import candidateForm, employerForm
from flask.ext.login import login_user, login_required
from flask import request, redirect, url_for, flash
from flask.ext.login import login_user, current_user

@app.route('/search')
def search():
    return render('search.html')
