from typing import List


class UserProfile(object):
    def __init__(self, id=None, username='', email=''):
        self._id = id
        self._username = username
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @id.setter
    def id(self, id):
        self._id = id

    @username.setter
    def username(self, username):
        self._username = username

    @email.setter
    def email(self, email):
        self._email = email
