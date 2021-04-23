from django.test import TestCase
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo
from apps.movie_quotes.infrastructure.django.models.SubtitleORM import SubtitleORM
from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.domain.entities.Subtitle import Subtitle
from apps.movie_quotes.domain.entities.Movie import Movie
from datetime import datetime

class TestSubtitle(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movie_orm =  MovieORM.objects.create(name = "", year = 2000, url = "")
        cls.subtitle_orm3 = SubtitleORM.objects.create(quote = "Monday is a bad day!!!",
                                                       start_time = datetime.now(),
                                                       end_time = datetime.now(),
                                                       movie = cls.movie_orm)
        cls.subtitle_orm1 = SubtitleORM.objects.create(quote = "Hello, Vasya!",
                                                       start_time = datetime.now(),
                                                       end_time = datetime.now(),
                                                       movie = cls.movie_orm)
        cls.subtitle_orm2 = SubtitleORM.objects.create(quote = "Hello, Petya!",
                                                       start_time = datetime.now(),
                                                       end_time = datetime.now(),
                                                       movie = cls.movie_orm)
    def setUp(self):
        pass

    def test_find_by_substring_in_quote(self):
        # Arrange
        quote = "Hello"
        expected_quotes = ["Hello, Vasya!", "Hello, Petya!"]
        subtitle_repo = SubtitleRepo()

        # Act
        subtitles = subtitle_repo.find_by_quote(quote)
        actual_quotes = [subtitle.quote for subtitle in subtitles]

        # Assert
        self.assertEqual(expected_quotes, actual_quotes)

    def test_find_by_substring_in_quote_all_matched(self):
        # Arrange
        quote = "!"
        expected_quotes = ["Monday is a bad day!!!", "Hello, Vasya!", "Hello, Petya!"]
        subtitle_repo = SubtitleRepo()

        # Act
        subtitles = subtitle_repo.find_by_quote(quote)
        actual_quotes = [subtitle.quote for subtitle in subtitles]

        # Assert
        self.assertEqual(expected_quotes, actual_quotes)

    def test_find_by_substring_in_quote_no_matched(self):
        # Arrange
        quote = "Good"
        expected_quotes = []
        subtitle_repo = SubtitleRepo()

        # Act
        subtitles = subtitle_repo.find_by_quote(quote)
        actual_quotes = [subtitle.quote for subtitle in subtitles]

        # Assert
        self.assertEqual(expected_quotes, actual_quotes)

    def test_get_subtitle(self):
        # Arrange
        quote = "I am a new one"
        subtitle_orm = SubtitleORM.objects.create(quote = quote,
                                                  start_time = datetime.now(),
                                                  end_time = datetime.now(),
                                                  movie = self.movie_orm)
        id = subtitle_orm.id
        expected_subtitle = {'id': id, 'quote': quote}
        subtitle_repo = SubtitleRepo()

        # Act
        subtitle = subtitle_repo.get(id)
        actual_subtitle = {'id': subtitle.id, 'quote': subtitle.quote}

        # Assert
        self.assertDictEqual(expected_subtitle, actual_subtitle)

    def test_create_subtitle(self):
        # Arrange
        movie_name = "Black swan"
        year = 2011
        url = "https://blackswan/"

        quote = "I am gonna die"

        movie = Movie(name = movie_name, year = year, url = url)
        subtitle = Subtitle(quote = quote, start_time = datetime.now(),
                            end_time = datetime.now(), movie = movie)
        expected_movie = {'name': movie_name, 'year': year, 'url': url}
        subtitle_repo = SubtitleRepo()

        # Act
        subtitle_repo.create(subtitle)
        subtitle_orm = SubtitleORM.objects.all().filter(quote = quote).first()

        # Assert
        self.assertIsNotNone(subtitle_orm)
        movie_orm = subtitle_orm.movie
        self.assertIsNotNone(movie_orm)
        actual_movie = {'name': movie_orm.name, 'year': movie_orm.year, 'url': movie_orm.url}
        self.assertDictEqual(expected_movie, actual_movie)