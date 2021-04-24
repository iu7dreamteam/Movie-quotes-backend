from django.test import TestCase
from django.contrib.auth.models import User

from apps.movie_quotes.infrastructure.django.TokenAuthorizer import TokenAuthorizer
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.domain.usecases.UserLoginUseCase import UserLoginUseCase, UserDoesNotExists
from rest_framework.authtoken.models import Token


class TestUserLoginUseCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_profile_repo = UserProfileRepo()
        cls.authorizer = TokenAuthorizer()

        cls.username = "FirstUsername"
        cls.email = "test@mail.ru"
        cls.password = "123123"

        cls.user = User.objects.create(username=cls.username,
                                       email=cls.email,
                                       password=cls.password)

        cls.token = Token.objects.get(user=cls.user).key


    def setUp(self):
        pass


    def test__execute_1(self):
        # Arrange
        expected_result = {
            'username': self.username,
            'token': self.token
        }

        # Act
        usecase = UserLoginUseCase(self.user_profile_repo,
                                   self.authorizer,
                                   self.email,
                                   self.password)

        actual_result = usecase.execute()

        # Assert
        self.assertDictEqual(expected_result, actual_result)


    def test__execute_UserDoesNotExists(self):
        # Arrange
        fake_email = "iamnotalive@void.su"
        fake_password = "tset"

        # Act
        usecase = UserLoginUseCase(self.user_profile_repo,
                                   self.authorizer,
                                   self.email,
                                   self.password)

        _ = usecase.execute()

        self.assertRaises(UserDoesNotExists)
