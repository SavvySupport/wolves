import os
# import Image
from app import app, savvy_collection
from app.Views.views import render
from flask.ext.login import login_required, current_user
from flask import jsonify, request, url_for, flash
from werkzeug import secure_filename
from hashlib import md5
from app.Helpers.Constant import *

@app.route('/dpupload', methods=['POST'])
@login_required
def dpupload():
    if request.method == 'POST':
        file = request.files['attachmentName']
        if file and allowed_file(file.filename):
            # Set up upload folder
            updir = os.path.join(app.config['basedir'], 'static/images/user/')

            # Delete old file
            delete_file = current_user.get_id().get(DP, None)
            if delete_file:
                delete_file = delete_file.split('/', -1)[-1]
                delete_file = os.path.join(updir, delete_file)
                if os.path.exists(delete_file):
                    os.remove(delete_file)

            # Get filename
            filename = secure_filename(file.filename)
            filename = md5((filename + current_user.get_id().get(EMAIL)).encode('utf-8')).hexdigest()

            # Check if user folder exists
            if not os.path.exists(updir):
                os.makedirs(updir)

            path = os.path.join(updir, filename)
            # Upload file to server
            file.save(path)

            # Resize image
            # install PIL with pip

            # Save path to database
            relative_path = os.path.join(url_for('static', filename='images/user/'), filename)
            user = { DP: relative_path }
            savvy_collection.update( {EMAIL: current_user.get_id().get(EMAIL)},
                                     {"$set": user} )


            # return information to frontend
            return jsonify(path=relative_path)

def allowed_file(filename):
    app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
