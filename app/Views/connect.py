import os
from app import app, savvy_collection
from app.Views.views import render
from flask.ext.login import login_required, current_user
from flask import jsonify, request, url_for, flash
from werkzeug import secure_filename
from hashlib import md5
from app.Helpers.Constant import *
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

@app.route('/connect', methods=['POST'])
@login_required
def connect():
    if request.method == 'POST':
        message = request.form['connectMsg']
        user = request.form['user']
        modal = request.form['modalId']

        #print(modal)
        user = savvy_collection.find_one( {EMAIL: user} )
        if user:
            # Send an email
            img_data = open('app/static/images/logo.png', 'rb').read()
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'An employer wants you!'
            msg['From'] = 'weiyew@savvysme.com.au'
            msg['To'] = user['email']
            From = 'weiyew@savvysme.com.au'
            To = user['email']

            text = """Dear {},\nAn employer is interested in your profile on SavvyHire and has a message for you!\nHere's the message:\n"{}"\nBest,\nTeam SavvyHire
            """.format(user['firstName'], message)

            bodyStyle = """
                background: #F3F4F5;
                padding: .71428571rem 1rem;
                box-shadow: none;
                border: 1px solid #D4D4D5;
                border-radius: .28571429rem;
                font-family: Lato,'Helvetica Neue',Arial,Helvetica,sans-serif;
            """
            greetStyle = """
                font-weight: 500;
                font-size: 27px;
            """
            contentStyle = """
                margin-bottom: 10px;
                margin-top: 5px;
                font-weight: normal;
                font-size: 17px;
                line-height: 1.6;
            """
            messageStyle = """
                margin-bottom: 4%;
                line-height: 2;
                display: block;
                background: #FFF;
                border: 1px solid rgba(133, 183, 217,.5);
                padding-top: 3%;
                padding-left: 7%;
                border-radius: 0.285714rem;
            """

            html = """\
            <html>
              <head></head>
              <body style="{}">
                <p><span style="{}">Dear {},<br><br></span>
                   <span style="{}">
                   An employer is interested in your profile on SavvyHire and has a message for you!<br><br>
                   Here's the message:<br><br>
                   <span style="{}"
                   <i>{}</i><br><br>
                   </span>
                   Best,<br>
                   Team SavvyHire<br>
                   </span>
                </p>
                <img src="https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-xap1/v/t1.0-9/12552797_946970445338090_4081041973572931633_n.png?oh=3657d0fd2ab010f7b752f825c16070ba&oe=572DAC6A&__gda__=1463629238_96cd9ea3062bfbbb1539e9cdfb18ad25" style="width:150px;">
              </body>
            </html>
            """.format(bodyStyle, greetStyle, user['firstName'], contentStyle, messageStyle, message)

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)

            image = MIMEImage(img_data, name=os.path.basename('app/static/images/logo.png'))
            msg.attach(image)

            s = smtplib.SMTP('smtp.gmail.com:587')
            username = "weiyew@savvysme.com.au"
            password = 'savvysme05464733'
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(username, password)
            s.sendmail(From, To, msg.as_string())
            s.quit()

        else:
            print('Nothing')
    return jsonify(result=modal)
