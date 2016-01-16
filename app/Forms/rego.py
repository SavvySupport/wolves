from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, validators, ValidationError

class regoForm(Form):
    username = TextField('username', [validators.length(min=5),
                                      validators.required(),
                                      validators.regexp('^[a-zA-Z0-9]+$')])
    password = PasswordField('password', [validators.length(min=5),
                                          validators.required()])
    confirm = PasswordField('passwordconfirm', [validators.equal_to('password')])
    email = TextField('email', [validators.required()])
