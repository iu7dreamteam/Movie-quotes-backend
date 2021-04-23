from django.test import TestCase
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo
from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.domain.entities.Movie import Movie

class TestMovieRepo(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_get_movie(self):
        # Arrange
        movie_name = "Black swan"
        year = 2011
        url = "https://blackswan/"
        movie_orm = MovieORM.objects.create(name = movie_name, year = year, url = url)
        id = movie_orm.id
        expected_movie = {'id': id, 'name': movie_name, 'year': year, 'url': url}
        movie_repo = MovieRepo()

        # Act
        movie_orm = movie_repo.get(id)
        actual_movie = {'id': movie_orm.id, 'name': movie_orm.name,
                        'year': movie_orm.year, 'url': movie_orm.url}

        # Assert
        self.assertDictEqual(expected_movie, actual_movie)

    def test_create_movie(self):
        # Arrange
        movie_name = "Black swan"
        year = 2011
        url = "https://blackswan/"

        quote = "I am gonna die"

        movie = Movie(name = movie_name, year = year, url = url)
        expected_movie = {'name': movie_name, 'year': year, 'url': url}
        movie_repo = MovieRepo()

        # Act
        movie_repo.create(movie)
        movie_orm = MovieORM.objects.all().filter(name = movie_name, year = year,
                                                  url = url).first()

        # Assert
        actual_movie = {'name': movie_orm.name, 'year': movie_orm.year, 'url': movie_orm.url}
        self.assertDictEqual(expected_movie, actual_movie)
