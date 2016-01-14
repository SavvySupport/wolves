class User:
    def is_authenticated(self):
        return False

    def is_active(self):
        return False

    def is_anonymous(self):
        return False

    def get_uid(self):
        return None

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
