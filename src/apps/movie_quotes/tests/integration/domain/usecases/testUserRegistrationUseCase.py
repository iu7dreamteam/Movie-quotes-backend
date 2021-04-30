from django.test import TestCase
from django.contrib.auth.models import User

from apps.movie_quotes.domain.usecases.UserRegistrationUseCase import UserRegistrationUseCase, UserAlreadyExists
from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.infrastructure.django.TokenAuthorizer import TokenAuthorizer


class TestUserRegistrationUseCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.authorizer = TokenAuthorizer()
        cls.user_profile_repo = UserProfileRepo()

    def setUp(self):
        pass

    def test__execute_1(self):
        # Arrange
        username = 'username'
        email = 'email123@mail.ru'
        password = '123123'

        # Act
        usecase = UserRegistrationUseCase(self.user_profile_repo, self.authorizer,
                                          username, email, password)
        
        actual_result = usecase.execute()

        # Assert
        self.assertEqual(username, actual_result['username'])
        self.assertEqual(email, actual_result['email'])
        self.assertIsNotNone(actual_result['token'])


    def test__execute_UserAlreadyExists__username(self):
        # Arrange
        username = "NewUser"
        email="first@mail.ru"
        password = "123"

        user = User.objects.create(username=username, email=email, password=password)

        # Act
        usecase = UserRegistrationUseCase(self.user_profile_repo, self.authorizer,
                                          username, "anotheremail@mail.ru", "anotherPassword")

        # Assert
        self.assertRaises(expected_exception=UserAlreadyExists)

    def test__execute_UserAlreadyExists__email(self):
        # Arrange
        username = "NewUser"
        email="first@mail.ru"
        password = "123"

        user = User.objects.create(username=username, email=email, password=password)

        # Act
        usecase = UserRegistrationUseCase(self.user_profile_repo, self.authorizer,
                                          "AnotherUsername", email=email, password="anotherPassword")

        # Assert
        self.assertRaises(expected_exception=UserAlreadyExists)
