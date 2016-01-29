import os
from app import app, savvy_collection
from app.Views.views import render
from flask.ext.login import login_required, current_user
from flask import jsonify, request, url_for, flash
from werkzeug import secure_filename
from hashlib import md5

@app.route('/connect', methods=['POST'])
@login_required
def connect():
    if request.method == 'POST':
        message = request.form['connectMsg']
        user = request.form['username']
        modal = request.form['modalId']

        print(modal)
        user = savvy_collection.find_one( {'username': user}, {'email': 1 } )
        if user:
            # Send an email
            pass
        else:
            print('Nothing')
    return jsonify(result=modal)
