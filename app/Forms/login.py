from wtforms import Form, TextField, PasswordField, validators
from app.Models.user import User
from app import savvy_collection

class loginForm(Form):
    username = TextField('username', [validators.required()])
    password = PasswordField('password', [validators.required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = savvy_collection.find_one({ "username": self.username.data })
        if user and User.validate_login(self.password, user['password']):
            return True
        else:
            return False
