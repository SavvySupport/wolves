from app import app, savvy_collection
from flask.ext.login import login_required
from flask import jsonify, request, url_for
from app.Helpers.Constant import *
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from bson.objectid import ObjectId
import os

@app.route('/apply', methods=['POST'])
@login_required
def applyJobs():
    if request.method == 'POST':
        print (request.form)
        message = request.form['applyJobMsg']
        employerId = request.form['employerId']
        employerId = ObjectId(employerId)
        modal = request.form['modalId']
        jobSeekerId = request.form['jobSeeker']
        jobSeekerId = ObjectId(jobSeekerId)
        title = request.form['title']

        #print(modal)
        jobSeeker = savvy_collection.find_one({'_id':jobSeekerId})
        user = savvy_collection.find_one( {'_id': employerId} )

        print (employerId)
        print (request.form)

        if user:
            # Send an email
            img_data = open('app/static/images/logo.png', 'rb').read()
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "{} {} applied for your {} position on SavvyHire".format(jobSeeker.get('firstName',''),jobSeeker.get('lastName','Someone'), title)
            msg['From'] = 'weiyew@savvysme.com.au'
            msg['To'] = user['email']
            From = 'weiyew@savvysme.com.au'
            To = user['email']

            text = """{} {} applied for your {} job!\nHere's the message:\n"{}"\nBest,\nTeam SavvyHire
            """.format(jobSeeker.get('firstName',''),jobSeeker.get('lastName','Someone'), title, message)

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
                padding: 1%;
                border-radius: 0.285714rem;
                white-space: PRE;
                word-wrap: break-word;
            """

            html = """\
            <html>
              <head></head>
              <body style="{}">
                <p><span style="{}">{} {} applied for your {} job!<br><br></span>
                   <span style="{}">
                   Here's their cover letter:<br><br>
                   <span style="{}"
                   <i>{}</i>
                   </span>
                   Here's the link to their digital cv:<br>
                   http://savvyhire.herokuapp.com/candidate/{}
                   <br><br>
                   Here's the email for you to contact directly: <a href="mailto:{}">{}</a>  <small style="color:rgb(17, 166, 86);">click it!</small>
                   <br><br>
                   Best,<br>
                   Team SavvyHire<br>
                   </span>
                </p>
                <img src="https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-xap1/v/t1.0-9/12552797_946970445338090_4081041973572931633_n.png?oh=3657d0fd2ab010f7b752f825c16070ba&oe=572DAC6A&__gda__=1463629238_96cd9ea3062bfbbb1539e9cdfb18ad25" style="width:150px;">
              </body>
            </html>
            """.format(bodyStyle, greetStyle, jobSeeker.get('firstName',''), jobSeeker.get('lastName','Someone'), title, contentStyle, messageStyle, message, str(jobSeekerId), jobSeeker.get('email',''), jobSeeker.get('email',''))
            #=============================================insert link of job seekers profile=========================
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
