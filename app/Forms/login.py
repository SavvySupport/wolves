from wtforms import Form, TextField, PasswordField, validators
from app.Models.User import User
from app import savvy_collection
from flask import flash
from flask.ext.login import login_user
from hashlib import md5
from app.Helpers.Constant import *

class loginForm(Form):
    username = TextField(USERNAME, [validators.required()])
    password = PasswordField(PASSWORD, [validators.required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            flash('Form invalid', 'error')
            return False

        # Query data from database
        user = savvy_collection.find_one({ USERNAME: self.username.data.rstrip() })

        if user:
            username = user.get(USERNAME, None)
            hash_password = user.get(PASSWORD, None)
            user_password = self.password.data.rstrip()
            account_token = user.get(TOKEN, '')

            if User.validate_login(hash_password, user_password):
                # if account_token == '':
                userObj = User(username)
                login_user(userObj)
                return True
                # else:
                    #if username and password is correct but have not validated Email
                    # flash('Please verify your email address', 'error')
        else:
            flash('Incorrect login credentials', 'error')
        return False
