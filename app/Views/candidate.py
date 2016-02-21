from app import app, savvy_collection, jobs_collection
from app.Views.views import render
from flask import request, redirect, url_for, flash
from app.Helpers.Constant import *
from bson.objectid import ObjectId

@app.route('/candidate/<uid>', methods=['GET'])
def candidate(uid):
    user = savvy_collection.find_one({ '_id': ObjectId(uid) })
    if user and user.get(CATEGORY) == CAND:
        return render('candidate.html', extra=user)
    else:
        flash('Invalid access to account', 'error')
        return redirect(url_for('home'))
