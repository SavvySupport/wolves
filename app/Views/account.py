from app import app, savvy_collection, jobs_collection
from app.Views.views import render
from app.Forms.account import candidateForm, employerForm
from flask.ext.login import login_user, login_required
from flask import request, redirect, url_for, flash
from flask.ext.login import login_user, current_user
from app.Helpers.Constant import *

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    username = current_user.get_id()[USERNAME]
    user = savvy_collection.find_one({ USERNAME: username })
    userJob = jobs_collection.find_one({'employerId':user.get('_id', '')})
    if user:
        form = None
        if user.get(CATEGORY, '') == EMPL:
            form = employerForm(username, request.form)
        elif user.get(CATEGORY, '') == CAND:
            form = candidateForm(username, request.form)

        if request.method == 'GET':
            form.prepopulate(user)

        if request.method == 'POST':
            if form.validate():
                flash('Successfully updated your profile', 'success')
                form.update(username)
            else:
                flash('Failed to update your profile', 'error')

        return render('account.html', form=form, error=None, extra=userJob)
    else:
        flash('Invalid access to account', 'error')
        return redirect(url_for('home'))
