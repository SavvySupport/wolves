from app import app
from app.Views.views import render
from flask.ext.login import login_user, current_user
from app.Forms.rego import regoForm
from flask import request, redirect, url_for
from app.Models.User import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('home'))

    form = regoForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('account'))

    return render('register.html', form=form)

#testing link http://127.0.0.1:5000/activate/weizteoh/b740538122a3bbcbece1467773034373
@app.route('/activate/<username>/<token>')
def activate(username, token):
    if User.validate_rego_token(username, token):
        login_user(User(username))
        return redirect(url_for('account'))
    return redirect(url_for('home'))
