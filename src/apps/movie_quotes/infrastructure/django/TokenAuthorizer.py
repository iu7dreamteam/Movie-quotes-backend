from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.domain.authorizer import Authorizer

from rest_framework.authtoken.models import Token


class TokenAuthorizer(Authorizer):

    def get_token(self, user_profile: UserProfile) -> str:
        user_profile_orm = UserProfileRepo().Mapper.from_domain(user_profile)
        token = Token.objects.get(user=user_profile_orm.user)
        return token.key
