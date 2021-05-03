from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.entities.Movie import Movie

from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo

from apps.movie_quotes.domain.usecases.UpdateUserHistoryUsecase import UpdateUserHistoryUsecase

from apps.movie_quotes.domain.serializers.MovieSerializer import MovieSerializer
from apps.movie_quotes.domain.serializers.SubtitleSerializer import SubtitleSerializer


class UpdateHistoryView(APIView):
    def post(self, request):
        try:
            token = request.COOKIES['token']
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            movie_id = request.data['movie_id']
            quote = request.data['quote']
            subtitles = request.data['subtitles']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_profile = UserProfileRepo().find_by_token(token)
        if user_profile is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        subtitle_repo = SubtitleRepo()
        subtitle_ids = [sub['id'] for sub in subtitles ]

        movie = MovieRepo().get(movie_id)
        subtitles = [subtitle_repo.get(id) for id in subtitle_ids]
        match = Match(
            quote=quote,
            movie=movie,
            subtitles=subtitles
        )

        usecase = UpdateUserHistoryUsecase(user_profile, match, MatchRepo())
        usecase.execute()

        return Response(status=status.HTTP_200_OK)
