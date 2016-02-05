from app import app, savvy_collection
from app.Views.views import render
from app.Forms.job import jobForm
from flask import request, redirect, url_for
from flask.ext.login import login_user, current_user, login_required
from app.Helpers.Constant import *

@app.route('/postJob', methods=['GET', 'POST'])
@login_required
def postJob():
    email = current_user.get_id()[EMAIL]
    user = savvy_collection.find_one({ EMAIL: email })
    if user and user.get(CATEGORY, None) == EMPL:
        form = jobForm(request.form)

        if request.method == 'POST' and form.validate():
            form.update(user)
            flash('successfully updated your job post')
            return redirect(url_for('account'))

        return render('job.html', form = form)
    else:
        flash('Invalid access to account', 'error')
        return redirect(url_for('home'))
