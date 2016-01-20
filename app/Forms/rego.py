from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators, ValidationError
from app.Models.User import User
from app import savvy_collection
from flask.ext.login import login_user
from flask import flash
from hashlib import md5
import os, subprocess


class regoAuthenticate():
    #to authenticate confirmation link
    def __init__(self, username, token):
        self.username = username
        self.token = token

    def validate(self):
        user = savvy_collection.find_one({ "username": self.username})
        if user['token'] == self.token and user['status'] == 'unverified':
            update = savvy_collection.update_one( {"username": self.username},
                                                  {"$set": {"status": "verified"}})

            flash('Your account has been verified!', 'success')
            return True
        elif user['token'] == self.token and user['status'] == 'verified':
            flash('Account has already been verified', 'warning')
            return False
        else:
            flash('Unknown confirmation link', 'error')
            return False

class regoForm(Form):
    username = TextField('username', [validators.length(min=5),
                                      validators.required(),
                                      validators.regexp('^[a-zA-Z0-9]+$')])
    password = PasswordField('password', [validators.length(min=5),
                                          validators.required()])
    confirm = PasswordField('passwordconfirm', [validators.equal_to('password')])
    email = TextField('email', [validators.required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            flash('Form invalid', 'error')
            return False

        user = savvy_collection.find_one({ "$or" : [ {"username": self.username.data.rstrip()},
                                                     {"email": self.email.data.rstrip()} ] })
        if user:
            flash('Email or Username has been taken', 'warning')
            return False
        else:
            token = md5(self.email.data.rstrip().encode('utf-8')).hexdigest()

            user = {
                "username": self.username.data.rstrip(),
                "password": md5(self.password.data.rstrip().encode('utf-8')).hexdigest(),
                "email"   : self.email.data.rstrip(),
                "status"  : "unverified",
                "token"   : token,
                "businessName": "",
                "contactName": "",
                "phoneNumber"   : "",
                "website"  : "",
                "streetAddress"   : "",
                "hiring"    : "",
                "firstName": "",
                "lastName": "",
                "gender"  : "",
                "birthday"   : "",
                "residency"    : "",
                "introduction"  : "",
                "education" : "",
                "availability"  : "",
                "skills"    : "" }

            # insert into database
            savvy_collection.insert(user)

#=======================Send confirmation email==================
            #url = os.getenv('SCRIPT_URI') <----------------get this to work when server is up
            url = '127.0.0.1:5000'
            message = """
            Hi {},

                You need to confirm your account by clicking this link:
                {}/confirmEmail/{}/{}

            Best,
            Team SavvyHire
            """.format(self.username.data.rstrip(),url, self.username.data.rstrip(), token)

            cmd="""echo '{}' | mail -s 'Confirm account' {}""".format(message, self.email.data.rstrip())
            p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            p.communicate()
#====================End of confirmation email===============

            # log in
            userObj = User(user['username'])
            login_user(userObj)

            return True
