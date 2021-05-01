from django.test import TestCase

from apps.movie_quotes.domain.serializers.MovieSerializer import MovieSerializer
from apps.movie_quotes.domain.entities.Movie import Movie
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM

from testfixtures import compare


class TestMovieSerializerWithRepo(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        cls.movie_1 = MovieRepo().get(cls.movie_orm_1.id)

    def setUp(self):
        pass

    def test__deserialize_movie_and_update_from_repo(self):
        # Arrange
        incomplete_movie_json = f'{{"id": "{self.movie_1.id}", \
"title": "{self.movie_1.title}", \
"director": "{self.movie_1.director}", \
"url": "{self.movie_1.video_url}"}}'

        # Act
        movie_serializer = MovieSerializer()
        incomplete_movie = movie_serializer.deserialize(incomplete_movie_json)

        movie_repo = MovieRepo()
        actual_movie = movie_repo.save(incomplete_movie)

        # Assert
        compare(self.movie_1, actual_movie)
