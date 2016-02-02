from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators, ValidationError
from app.Models.User import User
from app import savvy_collection
from flask import flash
from app.Helpers.Constant import *

class recoverForm(Form):
    email = TextField(EMAIL, [validators.required()])

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

        user = savvy_collection.find_one({ EMAIL : self.email.data.rstrip() })
        if user:
            # send email with new password to this address
            return True
        else:
            flash("{} doesn't exisit in our database".format(self.email.data), 'error')
            return False
