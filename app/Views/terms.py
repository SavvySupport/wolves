from app import app
from app.Views.views import render
from flask.ext.login import login_user, current_user
from flask import request, redirect, url_for
from app.Models.User import User

@app.route('/terms', methods=['GET'])
def terms():
    return render('terms.html')
