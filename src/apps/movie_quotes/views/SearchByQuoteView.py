from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.movie_quotes.domain.usecases.SearchByQuoteUsecase import SearchByQuoteUsecase
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo

# === Класс представления, реализующий post-запросы для получения результата поиска фильмов по цитате ===

class SearchByQuoteView(APIView):
    """
    **post** - запрос для получения результатов поиска фильмов по цитате
    """
    def post(self, request):
        # **Возвращаемый результат**
        try:
            quote = request.data['quote']
        except KeyError:
            
            try:
                quote = request.query_params['quote']
            except KeyError:
                """
                Отсутствие цитаты для поиска (некорректный запрос):
                
                - код 400
                
                - текст ошибки
                
                """
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data='Не обнаружено цитаты для поиска'
                )

        search_usecase = SearchByQuoteUsecase(
            MatchRepo(),
            SubtitleRepo(),
            quote
        )

        result = search_usecase.execute()

        """
        Успешный поиск фильмов по цитате:
            
        - код 200
            
        - словарь с данными о найденных фильмах
            
        """
        return Response(
            status=status.HTTP_200_OK,
            data=[match.to_dict() for match in result]
        )
