from app import app, savvy_collection, jobs_collection
from flask.ext.login import login_required, current_user
from flask import jsonify, request, json
from app.Helpers.Constant import *

@app.route('/editJob', methods=['POST'])
@login_required
def editJobPost():
    user = savvy_collection.find_one({ EMAIL: current_user.get_id()[EMAIL] })
    if user:
        if request.method == 'POST':
            print (request.data)
            print (request.form)
            print (request.json)
            jobId = request.json['jobId']
            listId = request.json['listId']
            position = request.json['position']
            availability = request.json['availability']
            residency = request.json['residency']
            location = request.json['location']
            description = request.json['description']
            print ('jobId = ' + jobId + ' listId = ' + listId)
            returnString = "#jobajax" + str(listId)

            employerId = user['_id']

            jobEntry = {
                TITLE       : position,
                AVAILABILITY: availability,
                DESCRIPTION : description,
                RESIDENCY   : residency,
                LOCATION    : location,
                EMPLOYERID  : employerId,
                TYPE        : JOB,
                BUSINESS    : user.get(BUSINESS,''),
                WEBSITE     : user.get(WEBSITE,''),
                ABOUT       : user.get(ABOUT,'')
            }

            jobs_collection.update({EMPLOYERID: employerId}, {"$set": {jobId: jobEntry}})

            print("Edited")

            # return information to frontend
            return jsonify(returnString = returnString)
