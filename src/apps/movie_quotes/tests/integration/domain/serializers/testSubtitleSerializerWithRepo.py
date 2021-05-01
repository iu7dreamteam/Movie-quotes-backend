from django.test import TestCase

from apps.movie_quotes.domain.serializers.SubtitleSerializer import SubtitleSerializer
from apps.movie_quotes.domain.entities.Subtitle import Subtitle
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo, SubtitleORM
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM

from testfixtures import compare

from datetime import datetime


class TestSubtitleSerializerWithRepo(TestCase):
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

    def test__deserialize_subtitle_and_update_from_repo(self):
        # Arrange
        incomplete_subtitle_json = f'{{"id": "{self.subtitle_1.id}", \
"quote": "{self.subtitle_1.quote}"}}'

        # Act
        subtitle_repo = SubtitleRepo()
        subtitle_serializer = SubtitleSerializer()

        incomplete_subtitle = subtitle_serializer.deserealize(incomplete_subtitle_json)
        actual_subtitle = subtitle_repo.save(incomplete_subtitle)

        # Assert
        compare(self.subtitle_1, actual_subtitle)
