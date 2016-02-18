from app import app, savvy_collection, jobs_collection
from flask.ext.login import login_required, current_user
from flask import jsonify, request, json
from app.Helpers.Constant import *

@app.route('/deleteJob', methods=['POST'])
@login_required
def deleteJobPost():
    user = savvy_collection.find_one({ EMAIL: current_user.get_id()[EMAIL] })
    if user:
        if request.method == 'POST':
            jobId = request.json['jobId']
            listId = request.json['listId']
            returnString = "#jobajax" + str(listId)
            employerId = user['_id']

            # Update savvy collection
            savvy_collection.update({EMAIL: user[EMAIL]},
                                    {"$pull": {'jobs': jobId}})

            # Delete job from job collection
            jobs_collection.update({EMPLOYERID: employerId},
                                   {"$unset": {jobId: ''}})

            # return information to frontend
            return jsonify(returnString = returnString)
