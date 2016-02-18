from wtforms import Form, PasswordField, validators, ValidationError
from app.Models.User import User
from app import savvy_collection
from flask import flash
from hashlib import md5
from app.Helpers.Constant import *

class changepasswordForm(Form):
    password = PasswordField(PASSWORD, [validators.length(min=5),
                                        validators.required()])
    passwordconfirm = PasswordField(PWDCONFIRM, [validators.equal_to(PASSWORD)])

    def __init__(self, *args, **kwargs):
        self.user = args[1]
        Form.__init__(self, args[0], **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            message = ''
            for fieldName, errorMessages in self.errors.items():
                for err in errorMessages:
                    message = message + fieldName + ': ' + err + '\n'
            flash(message, 'error')
            return False
        else:
            savvy_collection.update({EMAIL: self.user[EMAIL]},
                                    {"$set": {PASSWORD: md5(self.password.data.rstrip().encode('utf-8')).hexdigest()}})
            return True
