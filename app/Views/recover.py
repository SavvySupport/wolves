from app import app
from app.Forms.recover import recoverForm
from flask.ext.login import current_user
from flask import request, redirect, url_for
from app.Views.views import render

@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    form = recoverForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('login'))
    return render('recover.html', form=form)
