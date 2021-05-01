from django.test import TestCase
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo
from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.domain.entities.Movie import Movie


class TestMovieRepo(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.title = "Black swan"
        cls.year = 2011
        cls.director = "Darren Aronofsky"
        cls.poster_url = "https://blackswan/poster"
        cls.video_url = "https://blackswan/video"

    def setUp(self):
        pass

    def test_get_movie(self):
        # Arrange

        movie_orm = MovieORM.objects.create(title=self.title, year=self.year, director=self.director,
                                            poster_url=self.poster_url, video_url=self.video_url)
        id = movie_orm.id
        expected_movie = {'id': id, 'title': self.title, 'year': self.year, 'director': self.director,
                          'poster_url': self.poster_url, 'video_url': self.video_url}
        movie_repo = MovieRepo()

        # Act
        movie_orm = movie_repo.get(id)
        actual_movie = {'id': movie_orm.id, 'title': movie_orm.title,
                        'year': movie_orm.year, 'director': movie_orm.director,
                        'poster_url': movie_orm.poster_url, 'video_url': movie_orm.video_url}

        # Assert
        self.assertDictEqual(expected_movie, actual_movie)

    def test_save__new(self):
        # Arrange
        expected_movie_data = {
            'title': self.title,
            'year': self.year,
            'director': self.director,
            'poster_url': self.poster_url,
            'video_url': self.video_url
        }

        # Act
        movie = Movie(
            title=self.title,
            year=self.year,
            director=self.director,
            poster_url=self.poster_url,
            video_url=self.video_url
        )

        movie_repo = MovieRepo()
        actual_movie = movie_repo.save(movie)
        actual_movie_data = {
            'title': actual_movie.title,
            'year': actual_movie.year,
            'director': actual_movie.director,
            'poster_url': actual_movie.poster_url,
            'video_url': actual_movie.video_url
        }

        # Assert
        self.assertDictEqual(expected_movie_data, actual_movie_data)

    def test_save__update(self):
        # Arrange
        movie_orm = MovieORM.objects.create(
            title=self.title, 
            year=self.year,
            director=self.director,
            poster_url=self.poster_url,
            video_url=self.video_url
        )

        existed_movie = MovieRepo().get(movie_orm.id)

        title_new_value = 'The Departed'
        year_new_value = 2006
        director_new_value = 'Martin Scorsese'

        expected_movie_data = {
            'title': title_new_value,
            'year': year_new_value,
            'director': director_new_value,
            'poster_url': self.poster_url,
            'video_url': self.video_url
        }

        # Act
        existed_movie.title = title_new_value
        existed_movie.year = year_new_value
        existed_movie.director = director_new_value

        movie_repo = MovieRepo()
        actual_movie = movie_repo.save(existed_movie)
        actual_movie_data = {
            'title': actual_movie.title,
            'year': actual_movie.year,
            'director': actual_movie.director,
            'poster_url': actual_movie.poster_url,
            'video_url': actual_movie.video_url
        }
        
        self.assertDictEqual(expected_movie_data, actual_movie_data)

    def test_save__try_to_update_with_none_values(self):
        #
        #   In database fields with new values which are equal to None
        #   should not be overwritten because of the fact, that client tends to
        #   send back to server only a small part of object's data, such as ID.

        # Arrange
        movie_orm = MovieORM.objects.create(
            title=self.title,
            year=self.year,
            director=self.director,
            poster_url=self.poster_url,
            video_url=self.video_url
        )

        existed_movie = MovieRepo().get(movie_orm.id)

        expected_movie_data = {
            'title': self.title,
            'year': self.year,
            'director': self.director,
            'poster_url': self.poster_url,
            'video_url': self.video_url
        }

        # Act
        movie_repo = MovieRepo()

        existed_movie.title = None
        existed_movie.year = None
        existed_movie.director = None
        existed_movie.poster_url = None

        actual_movie = movie_repo.save(existed_movie)

        actual_movie_data = {
            'title': actual_movie.title,
            'year': actual_movie.year,
            'director': actual_movie.director,
            'poster_url': actual_movie.poster_url,
            'video_url': actual_movie.video_url
        }

        # Assert
        self.assertDictEqual(expected_movie_data, actual_movie_data)

        # Chech immutabilty direct in orm object
        actual_movie_orm = MovieORM.objects.get(pk=movie_orm.id)
        actual_movie_orm_data = {
            'title': actual_movie_orm.title,
            'year': actual_movie_orm.year,
            'director': actual_movie_orm.director,
            'poster_url': actual_movie_orm.poster_url,
            'video_url': actual_movie_orm.video_url
        }

        self.assertDictEqual(expected_movie_data, actual_movie_orm_data)
