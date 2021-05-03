from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo
from apps.movie_quotes.domain.usecases.ShowUserHistoryUsecase import ShowUserHistoryUsecase


class MatchHistoryView(APIView):
    def get(self, request, username):
        user_profile = UserProfileRepo().find_by_username(username)
        if user_profile is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data='Пользователь не найден'
            )

        show_history_usecase = ShowUserHistoryUsecase(
            user_profile=user_profile,
            user_profile_repo=UserProfileRepo(),
            match_repo=MatchRepo()
        )

        history = show_history_usecase.execute()

        history_dict = [match.to_dict() for match in history]

        return Response(
            status=status.HTTP_200_OK,
            data=history_dict
        )
