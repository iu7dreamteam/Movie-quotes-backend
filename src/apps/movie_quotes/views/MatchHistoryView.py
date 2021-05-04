from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo

from apps.movie_quotes.domain.usecases.ShowUserHistoryUsecase import ShowUserHistoryUsecase
from apps.movie_quotes.domain.usecases.UpdateUserHistoryUsecase import UpdateUserHistoryUsecase

from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo

# === Класс представления, реализующий get-запросы для получения истории поиска пользователя ===

class MatchHistoryView(APIView):
    """
    **get** - запрос для получения истории пользователя
    """
    def get(self, request, username):
        user_profile = UserProfileRepo().find_by_username(username)
        # **Возвращаемый результат**
        if user_profile is None:
            """
            Отсутствие пользователя с заданными данными:
            
            - код 404
            
            - текст ошибки
            
            """
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

        """
        Успешное получение истории:
            
        - код 200
            
        - словарь с данными о просмотренных фильмах и цитатах
            
        """
        return Response(
            status=status.HTTP_200_OK,
            data=history_dict
        )

    def post(self, request, username):
        """
        **post** - запрос на добавление матча в историю пользователя
        """

        try:
            token = request.COOKIES['token']
        except KeyError:
            # **Возвращаемый результат**
            """
            Пользователь не авторизован

            - код 401 

            """
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            movie_id = request.data['movie_id']
            quote = request.data['quote']
            subtitles = request.data['subtitles']
        except KeyError:
            """
            Невалидные данные о структуре Match, присланные клиентом

            - код 400 

            """
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

        """
        Успешное выполнение дополнения истории пользователя:

        - код 200

        """
        return Response(status=status.HTTP_200_OK)
