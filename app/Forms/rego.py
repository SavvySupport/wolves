from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField,\
                    validators, ValidationError, SelectField
from app.Models.User import User
from app import savvy_collection
from flask.ext.login import login_user
from flask import flash
from hashlib import md5
import os, subprocess

class regoForm(Form):
    username = TextField('username', [validators.length(min=5),
                                      validators.required(),
                                      validators.regexp('^[a-zA-Z0-9]+$')])
    password = PasswordField('password', [validators.length(min=5),
                                          validators.required()])
    confirm = PasswordField('passwordconfirm', [validators.equal_to('password')])
    email = TextField('email', [validators.required()])
    type = SelectField('type', choices=[('Employer', 'Employer'), ('Candidate', 'Candidate')], default='Candidate')

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
            raw_token = self.email.data + self.username.data + 'verification code'
            token = md5(raw_token.encode('utf-8')).hexdigest()
            user = {
                "username": self.username.data.rstrip(),
                "password": md5(self.password.data.rstrip().encode('utf-8')).hexdigest(),
                "email"   : self.email.data.rstrip(),
                "category"    : self.type.data,
                "token"   : token
            }

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
