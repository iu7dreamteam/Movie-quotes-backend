from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo

from apps.movie_quotes.domain.authorizer import Authorizer


class UserRegistrationUseCase:
    
    def __init__(self, 
                 user_profile_repo: UserProfileRepo,
                 authorizer: Authorizer,
                 username, email, password):

        self._user_profile_repo = user_profile_repo
        self._authorizer = authorizer
        self._username = username
        self._email = email
        self._password = password


    def execute(self) -> dict:
        if self._user_profile_repo.find_first_by_username(self._username) is not None:
            raise UserAlreadyExistsError(f"username {self._username}")

        if self._user_profile_repo.find_first_by_email(self._email) is not None:
            raise UserAlreadyExistsError(f"email {self._email}")

        user_profile = UserProfile(username=self._username, email=self._email)
        user_profile = self._user_profile_repo.create(user_profile, self._password)

        token = self._authorizer.get_token(user_profile)

        return {
            "username": user_profile.username,
            "email": user_profile.email,
            "token": token
        }


class UserAlreadyExists(Exception):
    def __init__(self, message=''):
        super().__init__("User with those parameters already exists: " + message)
