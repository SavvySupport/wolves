from app import app, savvy_collection
from app.Forms.changepassword import changepasswordForm
from flask.ext.login import login_user, current_user, login_required
from flask import request, redirect, url_for
from app.Views.views import render
from app.Models.User import User
from app.Helpers.Constant import *

@app.route('/changepassword/<email>/<password>', methods=['GET', 'POST'])
def changepassword(email, password):

    user = savvy_collection.find_one({ EMAIL: email })
    form = changepasswordForm(request.form,user)

    if user:
        if User.validate_password(email, password):
            print (user)
            print('validated')
            print(current_user.get_id())
            return render('change.html', form=form, extra=email)

    return redirect(url_for('home'))

@app.route('/change', methods=['GET','POST'])
def change():

    email = request.form['email']
    user = savvy_collection.find_one({ EMAIL: email })
    form=None
    if email:
        if user:
            form = changepasswordForm(request.form,user)

            if request.method == 'GET':
                return render('change.html', form=form)

            if request.method == 'POST' and form.validate():
                print('validated')
                return redirect(url_for('home'))

        return render('change.html', form=form, extra=email)
    else:
        return redirect(url_for('home'))
