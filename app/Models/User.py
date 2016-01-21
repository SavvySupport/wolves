from app import savvy_collection
from hashlib import md5
from flask import flash

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
    def validate_rego_token(username, token):
        user = savvy_collection.find_one({ 'username': username})
        if user:
            token_db = user.get('token', None)
            if token_db != None:
                if token_db == token:
                    update = savvy_collection.update_one( {'username': username}, {'$set': {'token': ''}} )
                    flash('Your account has been verified!', 'success')
                    return True
                elif token_db == '':
                    flash('Account has already been verified', 'warning')
                    return False

        flash('Unknown confirmation link', 'error')
        return False
