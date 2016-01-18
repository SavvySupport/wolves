from wtforms import Form, TextField, PasswordField, validators
from app.Models.user import User
from app import savvy_collection
from flask import flash
from flask.ext.login import login_user

class loginForm(Form):
    username = TextField('username', [validators.required()])
    password = PasswordField('password', [validators.required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            flash('Form invalid', 'error')
            return False

        user = savvy_collection.find_one({ "username": self.username.data.rstrip() })
        if user and User.validate_login(user['password'], self.password.data.rstrip()):
            userObj = User(user['username'])
            login_user(userObj)
            return True
        else:
            flash('Incorrect login credentials', 'error')
            return False
