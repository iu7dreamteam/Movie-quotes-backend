from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.movie_quotes.domain.usecases.SearchByQuoteUsecase import SearchByQuoteUsecase
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo


class SearchByQuoteView(APIView):
    def get(self, request):
        try:
            quote = request.data['quote']
        except KeyError:
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

        return Response(
            status=status.HTTP_200_OK,
            data=[match.to_dict() for match in result]
        )
