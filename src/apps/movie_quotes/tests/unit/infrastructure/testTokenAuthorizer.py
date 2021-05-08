from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.infrastructure.django.TokenAuthorizer import TokenAuthorizer


class TestTokenAuthorizer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_orm_1 = User.objects.create(username="username_1",
                                             email="email_1@mail.ru",
                                             password="123123")
        repo = UserProfileRepo()
        cls.user_profile_domain = repo.get(cls.user_orm_1.id)

    def setUp(self):
        pass

    def test__get_token(self):
        # Arrange
        expected_token = Token.objects.get(user=self.user_orm_1).key

        # Act
        actual_token = TokenAuthorizer().get_token(self.user_profile_domain)
        
        # Assert
        self.assertEqual(expected_token, actual_token)
