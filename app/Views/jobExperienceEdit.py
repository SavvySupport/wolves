from app import app, savvy_collection, jobs_collection
from flask.ext.login import login_required, current_user
from flask import jsonify, request, url_for, json
from app.Helpers.Constant import *

@app.route('/jobExperienceEdit', methods=['POST'])
@login_required
def jobExperienceEdit():
    user = savvy_collection.find_one({ EMAIL: current_user.get_id()[EMAIL] })

    if user:
        if request.method == 'POST':
            print (request.data)
            print (request.form)
            print (request.json)
            print("Edited")

            jobExperienceId = request.json['jobExperienceId']
            returnString = '#jobExperience'+jobExperienceId

            entry = {
                        'position'      : request.json['position'],
                        'company'       : request.json['company'],
                        'period'        : request.json['period'],
                        'description'   : request.json['description']
                    }

            old = user['jobExperience']
            print (old)
            old[str(jobExperienceId)] = entry
            print (old)
            savvy_collection.update({EMAIL:user[EMAIL]}, {"$set": {JOBEXPERIENCE: old}})
            
            # return information to frontend
            return jsonify(returnString = returnString)
