from wtforms import Form, TextField, PasswordField, validators
from app.Models.User import User
from app import savvy_collection
from flask import flash
from flask.ext.login import login_user
from hashlib import md5
from app.Helpers.Constant import *

class loginForm(Form):
    email = TextField(EMAIL, [validators.required()])
    password = PasswordField(PASSWORD, [validators.required()])

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

        # Query data from database
        user = savvy_collection.find_one({ EMAIL: self.email.data.rstrip() })

        if user:
            email = user.get(EMAIL, None)
            hash_password = user.get(PASSWORD, None)
            user_password = self.password.data.rstrip()
            account_token = user.get(TOKEN, '')

            if User.validate_login(hash_password, user_password):
                userObj = User(email)
                login_user(userObj)
                return True
        else:
            flash('Incorrect login credentials', 'error')
        return False
