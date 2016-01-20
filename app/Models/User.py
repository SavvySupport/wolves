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
        user = savvy_collection.find_one({ "username": username})
        if user['token'] == token and user['status'] == 'unverified':
            update = savvy_collection.update_one( {"username": username},
                                                  {"$set": {"status": "verified"}})

            flash('Your account has been verified!', 'success')
            return True
        elif user['token'] == token and user['status'] == 'verified':
            flash('Account has already been verified', 'warning')
            return False
        else:
            flash('Unknown confirmation link', 'error')
            return False
