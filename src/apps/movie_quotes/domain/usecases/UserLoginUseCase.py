from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo

from apps.movie_quotes.domain.authorizer import Authorizer


class UserLoginUseCase:
    def __init__(self, user_profile_repo: UserProfileRepo,
                 authorizer: Authorizer,
                 email, password):

        self._user_profile_repo = user_profile_repo
        self._authorizer = authorizer
        self._email = email
        self._password = password


    def execute(self) -> dict:
        user_profile = self._user_profile_repo.find_by_email(self._email)
        if user_profile is None:
            raise UserDoesNotExists()

        if not self._user_profile_repo.check_password(user_profile, self._password):
            raise IncorrectPassword()

        token = self._authorizer.get_token(user_profile)

        return {
            'username': user_profile.username,
            'email': user_profile.email,
            'token': token
        }


class UserDoesNotExists(Exception):
    def __init__(self, message=''):
        super().__init__("User with those parameters does not exists" + message)

class IncorrectPassword(Exception):
    def __init__(self, message=''):
        super().__init__("Given password is not correct" + message)
