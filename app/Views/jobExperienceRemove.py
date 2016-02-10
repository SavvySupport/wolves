import os
from app import app, savvy_collection, jobs_collection
from app.Views.views import render
from flask.ext.login import login_required, current_user
from flask import jsonify, request, url_for, json
from werkzeug import secure_filename
from hashlib import md5
from app.Helpers.Constant import *


@app.route('/jobExperienceRemove', methods=['POST'])
@login_required
def jobExperienceRemove():

    user = savvy_collection.find_one({ EMAIL: current_user.get_id()[EMAIL] })

    if user:
        if request.method == 'POST':
            print (request.data)
            print (request.form)
            print (request.json)
            print("Deleted")
            jobExperienceId = request.json['jobExperienceId']
            returnString = '#jobExperience'+jobExperienceId

            old = user['jobExperience']
            del old[jobExperienceId]
            savvy_collection.update({EMAIL:user['email']},{"$set":{JOBEXPERIENCE:old}})



    #            # return information to frontend
            return jsonify(returnString = returnString)
