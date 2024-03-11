
class User(object):
    def __init__(self, user_name, password, email):
        self.user_name = user_name
        self.password = password
        self.email = email

    def to_dict(self):
        return {
            'user_name': self.user_name,
            'email': self.email,
            'password': self.password
        }
