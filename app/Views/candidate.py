from app import app, savvy_collection, jobs_collection
from app.Views.views import render
from app.Forms.account import candidateForm
from flask.ext.login import login_user, login_required
from flask import request, redirect, url_for, flash
from flask.ext.login import login_user, current_user
from app.Helpers.Constant import *

@app.route('/candidate/<email>', methods=['GET', 'POST'])
def candidate(email):
    user = savvy_collection.find_one({ EMAIL: email })
    if user and user.get(CATEGORY) == CAND:
        form = candidateForm(user, request.form)
        if request.method == 'GET':
            form.prepopulate(user)

        return render('candidate.html', form=form, extra=user)
    else:
        flash('Invalid access to account', 'error')
        return redirect(url_for('home'))
