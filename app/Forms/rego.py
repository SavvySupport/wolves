from wtforms import Form, BooleanField, TextField, PasswordField,\
                    validators, ValidationError, SelectField
from app.Models.User import User
from app import savvy_collection, jobs_collection
from flask.ext.login import login_user
from flask import flash
from hashlib import md5
from app.Helpers.Constant import *

class regoForm(Form):
    email = TextField(EMAIL, [validators.required()])
    password = PasswordField(PASSWORD, [validators.length(min=5),
                                        validators.required()])
    confirm = PasswordField(PWDCONFIRM, [validators.equal_to(PASSWORD)])
    #category = SelectField(CATEGORY, choices = [EMPLOYER, CANDIDATE],
    #                                 default = CANDIDATE[TEXT])
    category = SelectField(CATEGORY, choices = [CANDIDATE],
                                     default = CANDIDATE[TEXT])
    termsConditions = BooleanField(TERMSCOND, [validators.required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            message = ''
            for fieldName, errorMessages in self.errors.items():
                for err in errorMessages:
                    message = message + fieldName + ': ' + err + '\n'
            flash(message, 'error')
            return False

        user = savvy_collection.find_one({EMAIL: self.email.data.rstrip()})
        if user:
            flash('Email has already been taken', 'warning')
            return False
        else:
            raw_token = self.email.data + 'verification code'
            token = md5(raw_token.encode('utf-8')).hexdigest()
            user = {
                PASSWORD      : md5(self.password.data.rstrip().encode('utf-8')).hexdigest(),
                EMAIL         : self.email.data.rstrip(),
                CATEGORY      : self.category.data,
                TOKEN         : token
            }

            # insert into database
            employerId = savvy_collection.insert_one(user).inserted_id

            if self.category.data == EMPL:
                jobs_collection.insert({EMPLID: employerId})

            #url = os.getenv('SCRIPT_URI') <----------------get this to work when server is up
            # url = '127.0.0.1:5000'
            # message = """
            # Hi {},
            #
            #     You need to confirm your account by clicking this link:
            #     {}/confirmEmail/{}/{}
            #
            # Best,
            # Team SavvyHire
            # """.format(self.username.data.rstrip(),url, self.username.data.rstrip(), token)
            #
            # cmd="""echo '{}' | mail -s 'Confirm account' {}""".format(message, self.email.data.rstrip())
            # p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            # p.communicate()

            # log in
            userObj = User(user[EMAIL])
            login_user(userObj)

            return True
