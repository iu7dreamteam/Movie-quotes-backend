from django.test import TestCase, TransactionTestCase

from apps.movie_quotes.domain.repositories.MovieRepo import Movie, MovieORM, MovieRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import Subtitle, SubtitleORM, SubtitleRepo

from apps.movie_quotes.utility.subtitle_parser import SubtitleParser

from rest_framework import status

import os


class TestSearchWithoutAuthentication(TransactionTestCase):
    reset_sequences = True
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_scenario(self):
        # *********************** Populate the database *******************
        movie_LOTR = MovieRepo().save(
            Movie(
                title='The Lord of the Rings',
                year=2001,
                director='Peter Jackson',
                poster_url='http://someurl/',
                video_url='http://anotherurl/'
            )
        )

        subtitles_LOTR = SubtitleParser.parse(os.path.dirname(__file__) + '/res/LOTR.en.srt')

        subtitle_repo = SubtitleRepo()
        for sub in subtitles_LOTR:
            sub.movie = movie_LOTR
            subtitle_repo.save(sub)
        # -----------------------------------------------------------------

        # Arrange
        search_quote = "Run, Frodo"
        expected_json = [{
            "quote": search_quote,
            "movie": {
                "id": "1",
                "title": 'The Lord of the Rings',
                "year": "2001",
                "director": "Peter Jackson",
                "poster": 'http://someurl/',
                "url": 'http://anotherurl/'
            },
            "quotes": [
                {
                    "id": "652",
                    "quote": "Run, Frodo!",
                    "time": "00:56:54.940000"
                },
                {
                    "id": "1712",
                    "quote": "Run, Frodo. Go!",
                    "time": "03:06:04.190000"
                }
            ]
        }]

        request_data = {
            "quote": search_quote
        }

        # Act
        resp = self.client.get('/api/v0/movies/quote/', request_data, format='json')

        # Assert
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_json, resp.data)

    def _cleanup_database(self):
        MovieORM.objects.all().delete()
