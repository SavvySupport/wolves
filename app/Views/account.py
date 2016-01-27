from app import app, savvy_collection
from app.Views.views import render
from app.Forms.account import candidateForm, employerForm
from flask.ext.login import login_user, login_required
from flask import request, redirect, url_for, flash
from flask.ext.login import login_user, current_user

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    username = current_user.get_id()['username']
    user = savvy_collection.find_one({ "username": username })
    if user:
        form = None
        if user.get('category', '').lower() == 'employer':
            form = employerForm(username, request.form)
        elif user.get('category', '').lower() == 'candidate':
            form = candidateForm(username, request.form)

        if request.method == 'GET':
            form.prepopulate(user)

        if request.method == 'POST':
            if form.validate():
                flash('Successfully updated your profile', 'success')
                form.update(username)
            else:
                flash('Failed to update your profile', 'error')

        return render('account.html', form=form)
    else:
        flash('Invalid access to account', 'error')
        return redirect(url_for('home'))
