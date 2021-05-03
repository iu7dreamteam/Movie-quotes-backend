from django.test import TestCase

from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo, User
from apps.movie_quotes.domain.entities.UserProfile import UserProfile

from rest_framework.authtoken.models import Token

from testfixtures import compare


class TestUserProfileRepo(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test__find_by_token(self):
        # Arrange
        user_orm = User.objects.create(username='testuser', email='testemail@yandex.ru', password='123123')
        token = Token.objects.get(user=user_orm).key
        expected_user_profile = UserProfileRepo().get(user_orm.id)

        # Act
        user_profile_repo = UserProfileRepo()
        actual_user_profile = user_profile_repo.find_by_token(token)

        # Assert
        compare(expected_user_profile, actual_user_profile)
