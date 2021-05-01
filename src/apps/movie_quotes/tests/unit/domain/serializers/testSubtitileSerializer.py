from django.test import TestCase

from apps.movie_quotes.domain.serializers.SubtitleSerializer import SubtitleSerializer
from apps.movie_quotes.domain.entities.Subtitle import Subtitle
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleORM, SubtitleRepo
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM

from testfixtures import compare

from datetime import datetime, time


class TestSubtitleSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        cls.subtitle_orm1 = SubtitleORM.objects.create(quote = "Monday is a bad day!!!",
                                                       start_time = datetime.now(),
                                                       end_time = datetime.now(),
                                                       movie = cls.movie_orm_1)

        cls.movie_1 = MovieRepo().get(cls.movie_orm_1.id)
        cls.subtitle_1 = SubtitleRepo().get(cls.subtitle_orm1.id)

    def setUp(self):
        pass

    def test__subtitle_serialization(self):
        # Arrange
        expected_subtitle_json = f'{{"id": "{self.subtitle_1.id}", \
"quote": "{self.subtitle_1.quote}", \
"time": "{self.subtitle_1.start_time}"}}'

        # Act
        subtitle_serializer = SubtitleSerializer()
        actual_subtitle_json = subtitle_serializer.serialize(self.subtitle_1)

        self.assertJSONEqual(expected_subtitle_json, actual_subtitle_json)

    def test__subtitle_deserialization(self):
        # Arrange
        subtitle_json = f'{{"id": "{self.subtitle_1.id}", "quote": "{self.subtitle_1.quote}"}}'

        expected_subtitle = Subtitle(
            id=self.subtitle_1.id,
            quote=self.subtitle_1.quote,
            start_time=None,
            end_time=None,
            movie=None
        )

        # Act
        subtitle_serializer = SubtitleSerializer()
        actual_subtitle = subtitle_serializer.deserealize(subtitle_json)

        compare(expected_subtitle, actual_subtitle)
