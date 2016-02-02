from app import app, savvy_collection
from app.Views.views import render
from app.Forms.account import candidateForm, employerForm
from flask.ext.login import login_user, login_required
from flask import request, redirect, url_for, flash, jsonify
from flask.ext.login import login_user, current_user
from app.Helpers.Constant import *

@app.route('/search')
@login_required
def search():
    # Query all available candidates
    candidates = savvy_collection.find({ CATEGORY: CAND }) 
    return render('search.html', jsonObject=candidates)
