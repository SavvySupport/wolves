import os
from app import app, savvy_collection, jobs_collection
from app.Views.views import render
from flask.ext.login import login_required, current_user
from flask import jsonify, request, url_for, json
from werkzeug import secure_filename
from hashlib import md5
from app.Helpers.Constant import *


@app.route('/deleteJob', methods=['POST'])
@login_required
def deleteJob():

    user = savvy_collection.find_one({ EMAIL: current_user.get_id()[EMAIL] })

    if user:
        if request.method == 'POST':
            print (request.data)
            print (request.form)
            print (request.json)
            jobId = request.json['jobId']
            listId = request.json['listId']
            print ('jobId = ' + jobId + ' listId = ' + listId)
            returnString = "#jobajax" + str(listId)

            employerId = user['_id']

            savvy_collection.update({EMAIL:user['email']},{"$pull":{'jobs': jobId}})
            jobs_collection.update({EMPLOYERID:employerId},{"$unset":{jobId:''}})

            print("Deleted")

    #            # return information to frontend
            return jsonify(returnString = returnString)
