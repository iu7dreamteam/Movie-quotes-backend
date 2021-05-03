from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.infrastructure.django.models.UserProfileORM import UserProfileORM, User

from rest_framework.authtoken.models import Token

from django.core.exceptions import ObjectDoesNotExist


class UserProfileRepo:
    def get(self, id) -> UserProfile:
        user_profile_orm = UserProfileORM.objects.get(user_id=id)
        return self.Mapper.to_domain(user_profile_orm)

    def create(self, user_profile: UserProfile, password) -> UserProfile:
        user_orm = User.objects.create_user(
            username=user_profile.username,
            email=user_profile.email,
            password=password
        )

        return self.Mapper.to_domain(UserProfileORM.objects.get(user=user_orm))

    def find_by_username(self, username) -> UserProfile:
        user_orm = User.objects.filter(username=username).first()
        if user_orm is not None:
            return self.get(id=user_orm.id)
        return None

    def find_by_email(self, email) -> UserProfile:
        user_orm = User.objects.filter(email=email).first()
        if user_orm is not None:
            return self.get(id=user_orm.id)
        return None

    def find_by_token(self, token) -> UserProfile:
        try:
            token = Token.objects.get(key=token)
            user_orm = token.user
            return self.get(id=user_orm.id)
        except ObjectDoesNotExist:
            return None

    def check_password(self, user_profile: UserProfile, password: str) -> bool:
        user_profile_orm = self.Mapper.from_domain(user_profile)
        result = user_profile_orm.user.check_password(password)
        return result

    class Mapper:
        @staticmethod
        def to_domain(user_profile_orm: UserProfileORM) -> UserProfile:
            return UserProfile(
                id=user_profile_orm.id,
                username=user_profile_orm.user.username,
                email=user_profile_orm.user.email
            )

        @staticmethod
        def from_domain(user_profile: UserProfile) -> UserProfileORM:
            return UserProfileORM.objects.get(pk=user_profile.id)
