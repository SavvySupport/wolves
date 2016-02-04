from app import savvy_collection
from hashlib import md5
from flask import flash, url_for
from app.Helpers.Constant import *

class User():
    def __init__(self, userObj):
        self.user = userObj

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user

    @staticmethod
    def validate_login(password_hash, password):
        return md5(password.encode('utf-8')).hexdigest() == password_hash

    @staticmethod
    def validate_rego_token(email, token):
        user = savvy_collection.find_one({ EMAIL: email })
        if user:
            token_db = user.get(TOKEN, None)
            if token_db != None:
                if token_db == token:
                    update = savvy_collection.update_one( {EMAIL: email}, {'$set': {TOKEN: ''}} )
                    flash('Your account has been verified!', 'success')
                    return True
                elif token_db == '':
                    flash('Account has already been verified', 'warning')
                    return False

        flash('Unknown confirmation link', 'error')
        return False

    def validate_password(email, password):
        user = savvy_collection.find_one({ EMAIL: email })
        return user[PASSWORD] == password
