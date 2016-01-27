from app import app
from flask.ext.login import logout_user
from flask import redirect, url_for

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
