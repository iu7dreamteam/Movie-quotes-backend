from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.infrastructure.django.models.UserProfileORM import UserProfileORM, User


class UserProfileRepo:

    def get(self, id) -> UserProfile:
        user_profile_orm = UserProfileORM.objects.get(pk=id)
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

    def find_by_email(self, email) -> UserProfile:
        user_orm = User.objects.filter(email=email).first()
        if user_orm is not None:
            return self.get(id=user_orm.id)


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
