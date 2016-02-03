from app import app
from app.Views.views import render
from app.Forms.login import loginForm
from flask.ext.login import login_user
from flask import request, redirect, url_for
from flask.ext.login import login_user, current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Case: user is already logged in
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    # Case: user submits form
    form = loginForm(request.form)
    if request.method == 'POST' and form.validate():
        print('validated')
        if request.form.get('next') != None and request.form.get('next') != 'None':
            return redirect(request.form.get('next'))
        else:
            return redirect(url_for('home'))

    # Case: user needs to log in
    return render('login.html', form)
