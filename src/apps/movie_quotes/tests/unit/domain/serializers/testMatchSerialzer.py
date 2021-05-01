from django.test import TestCase

from apps.movie_quotes.domain.serializers.MatchSerializer import MatchSerializer
from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo, MatchORM
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo, SubtitleORM

from testfixtures import compare

from datetime import time


class TestMatchSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        subtitle_orm1 = SubtitleORM.objects.create(quote = "Monday is a bad day!!!",
                                                   start_time = time(hour=0, minute=0, second=37, microsecond=673000),
                                                   end_time = time(hour=0, minute=0, second=39, microsecond=673000),
                                                   movie = movie_orm_1)
        subtitle_orm2 = SubtitleORM.objects.create(quote = "Also Monday is a good day",
                                                   start_time = time(hour=0, minute=1, second=37, microsecond=673000),
                                                   end_time = time(hour=0, minute=0, second=59, microsecond=673001),
                                                   movie = movie_orm_1)

        cls.movie_1 = MovieRepo().get(movie_orm_1.id)
        cls.sub_1 = SubtitleRepo().get(subtitle_orm1.id)
        cls.sub_2 = SubtitleRepo().get(subtitle_orm2.id)

        cls.match = Match(
            movie=cls.movie_1,
            subtitles=[cls.sub_1, cls.sub_2]
        )

    def setUp(self):
        pass

    def test__serialize_match(self):
        # Arrange
        expected_json = '{"movie": {"id": "1", "title": "bomonka1", \
"year": "2001", "director": "me", \
"poster": "https://bmstu.ru", "url": "https://bmstu.ru/poster.png"}, \
"quotes": [{"id": "1", "quote": "Monday is a bad day!!!", "time": "00:00:37.673000"}, \
{"id": "2", "quote": "Also Monday is a good day", "time": "00:01:37.673000"}]}'

        # Act
        match_serializer = MatchSerializer()
        actual_json = match_serializer.serialize(self.match)

        # Assert
        compare(expected_json, actual_json)
