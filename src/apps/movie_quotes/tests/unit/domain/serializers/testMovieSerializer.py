from django.test import TestCase

from apps.movie_quotes.domain.serializers.MovieSerializer import MovieSerializer
from apps.movie_quotes.domain.entities.Movie import Movie
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM

from testfixtures import compare


class TestMovieSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        cls.movie_1 = MovieRepo().get(cls.movie_orm_1.id)

    def setUp(self):
        pass

    def test_movie_serialization(self):
        # Arrange
        expected_movie_json = f'{{"id": "{self.movie_1.id}", \
"title": "{self.movie_1.title}", \
"year": "{self.movie_1.year}", \
"director": "{self.movie_1.director}", \
"poster": "{self.movie_1.poster_url}", \
"url": "{self.movie_1.video_url}"}}'

        # Act
        movie_serializer = MovieSerializer()
        actual_movie_json = movie_serializer.serialize(self.movie_1)

        # Assert
        self.assertJSONEqual(expected_movie_json, actual_movie_json)

    def test_movie_deserialization(self):
        # Arrange
        movie_json = f'{{"id": "{self.movie_1.id}", \
"title": "{self.movie_1.title}", \
"year": "{self.movie_1.year}", \
"director": "{self.movie_1.director}", \
"poster": "{self.movie_1.poster_url}", \
"url": "{self.movie_1.video_url}"}}'

        expected_movie = Movie(
            id=self.movie_1.id,
            title=self.movie_1.title,
            year=self.movie_1.year,
            director=self.movie_1.director,
            poster_url=self.movie_1.poster_url,
            video_url=self.movie_1.video_url
        )

        # Act
        movie_serializer = MovieSerializer()
        actual_movie = movie_serializer.deserialize(movie_json)

        # Assert
        compare(expected_movie, actual_movie)
