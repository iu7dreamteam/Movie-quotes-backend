from typing import List

# === Модель бизнес-логики для описания субтитра ===

class UserProfile(object):
    def __init__(self, id=None, username='', email=''):
        self._id = id
        self._username = username
        self._email = email

    """
    Поля Movie:
    
    - id - идентификатор субтитра
    
    - username - имя пользователя
    
    - email - почта пользователя
    
    """

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
