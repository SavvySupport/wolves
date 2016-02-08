from app import app, savvy_collection
from app.Views.views import render
from app.Forms.jobs import jobForm
from flask import request, redirect, url_for
from flask.ext.login import login_user, current_user
from app.Helpers.Constant import *

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    email = current_user.get_id()[EMAIL]
    user = savvy_collection.find_one({ EMAIL: email })
    if user:
        form = None

        if user.get(CATEGORY, None) == EMPL:
            form = jobForm(request.form, user[EMAIL])
        else:
            return redirect(url_for('home'))

        if request.method == 'POST' and form.validate(user):
            return redirect(url_for('account'))

        return render('jobs.html', form = form)

    else:
        flash('Invalid access to account', 'error')
        return redirect(url_for('home'))
