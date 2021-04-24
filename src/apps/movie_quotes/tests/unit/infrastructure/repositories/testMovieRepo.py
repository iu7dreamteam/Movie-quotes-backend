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
        director = "Darren Aronofsky"
        poster_url = "https://blackswan/poster"
        video_url = "https://blackswan/video"
        movie_orm = MovieORM.objects.create(title = movie_name, year = year, director = director,
                                            poster_url = poster_url, video_url = video_url)
        id = movie_orm.id
        expected_movie = {'id': id, 'title': movie_name, 'year': year, 'director': director,
                          'poster_url': poster_url, 'video_url': video_url}
        movie_repo = MovieRepo()

        # Act
        movie_orm = movie_repo.get(id)
        actual_movie = {'id': movie_orm.id, 'title': movie_orm.title,
                        'year': movie_orm.year, 'director': movie_orm.director,
                        'poster_url': movie_orm.poster_url, 'video_url': movie_orm.video_url}

        # Assert
        self.assertDictEqual(expected_movie, actual_movie)

    def test_create_movie(self):
        # Arrange
        movie_name = "Black swan"
        year = 2011
        director = "Darren Aronofsky"
        poster_url = "https://blackswan/poster"
        video_url = "https://blackswan/video"
        movie = Movie(title = movie_name, year = year, director = director,
                      poster_url = poster_url, video_url = video_url)
        expected_movie = {'title': movie_name, 'year': year, 'director': director,
                          'poster_url': poster_url, 'video_url': video_url}
        movie_repo = MovieRepo()

        # Act
        movie_repo.create(movie)
        movie_orm = MovieORM.objects.all().filter(title = movie_name, year = year, director = director,
                                                  poster_url = poster_url, video_url = video_url).first()

        # Assert
        actual_movie = {'title': movie_orm.title,
                        'year': movie_orm.year, 'director': movie_orm.director,
                        'poster_url': movie_orm.poster_url, 'video_url': movie_orm.video_url}
        self.assertDictEqual(expected_movie, actual_movie)
