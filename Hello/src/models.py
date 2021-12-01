from src import db
import hashlib

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    useremail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    # @property
    # def password(self):
    #     raise AttributeError('password not readable')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = hashlib.sha256(password.encode())
        # or whatever other hashing function you like.

    # def verify_password(self, password)
    #     return some_check_hash_func(self.password_hash, password)