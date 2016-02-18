from app import app, savvy_collection
from app.Views.views import render
from flask.ext.login import login_required, current_user
from flask import jsonify, request, url_for, json
from app.Helpers.Constant import *
from collections import OrderedDict

@app.route('/jobExperience', methods=['POST'])
@login_required
def jobExperience():
    user = savvy_collection.find_one({ EMAIL: current_user.get_id()[EMAIL] })
    if user:
        if request.method == 'POST':
            print(request.data)
            print(request.form)
            print(request.json)
            print("Deleted")
            
            returnString = request.json
            company = request.json['company']
            period = request.json['period']
            position = request.json['position']
            description = request.json['description']

            entry = {
                        'position'      : position,
                        'company'       : company,
                        'period'        : period,
                        'description'   : description
                    }

            oldDic = user.get('jobExperience')
            if oldDic:
                newIndex = int(max(oldDic.keys()))
                newDic = OrderedDict()
                newDic = oldDic
                newDic[str(newIndex + 1)] = entry
                savvy_collection.update({EMAIL:user[EMAIL]},{"$set":{'jobExperience':newDic}})

            else:
                oldDic = OrderedDict()
                oldDic['1'] = entry
                savvy_collection.update({EMAIL:user[EMAIL]},{"$set":{'jobExperience':oldDic}})

            # return information to frontend
            return jsonify(returnString = returnString)
