from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators, ValidationError
from app.Models.user import User
from app import savvy_collection
from flask import flash

class recoverForm(Form):
    email = TextField('email', [validators.required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            flash('Form invalid', 'error')
            return False

        user = savvy_collection.find_one({ "email": self.email.data })
        if user:
            # change password to a random string
            
            # send email with new password to this address
            return True
        else:
            flash("{} doesn't exisit in our database".format(self.email.data))
            return False
