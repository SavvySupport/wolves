from app import app, savvy_collection, jobs_collection
from app.Views.views import render
from app.Forms.account import candidateForm, employerForm
from flask.ext.login import login_user, login_required
from flask import request, redirect, url_for, flash, jsonify
from flask.ext.login import login_user, current_user
from app.Helpers.Constant import *

@app.route('/jobs')
@login_required
def jobSearch():
    # display all jobs 
    jobs = jobs_collection.find()
    jobsDict = {}
    for elements in jobs:
        elements.pop('employerId', None)
        elements.pop('_id', None)
        jobsDict.update(elements)

    return render('jobSearch.html', extra=jobsDict)
