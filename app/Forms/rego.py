from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators, ValidationError
from app.Models.user import User
from app import savvy_collection
from flask.ext.login import login_user
from flask import flash

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

        user = savvy_collection.find_one({ "$or" : [ {"username": self.username.data},
                                                     {"email": self.email.data} ] })


        if user:
            flash('Email or Username has been taken', 'warning')
            return False
        else:
            user = {
                "username": self.username.data,
                "password": self.password.data,
                "email"   : self.email.data }

            # insert into database
            savvy_collection.insert(user)

            # log in
            userObj = User(user['username'])
            login_user(userObj)

            return True
