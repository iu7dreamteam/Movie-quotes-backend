from django.test import TestCase, TransactionTestCase

from apps.movie_quotes.domain.repositories.MovieRepo import Movie, MovieORM, MovieRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import Subtitle, SubtitleORM, SubtitleRepo
from apps.movie_quotes.domain.repositories.UserProfileRepo import User

from apps.movie_quotes.utility.subtitle_parser import SubtitleParser

from rest_framework import status

import os
import json


class TestFullUsecase(TransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_scenario(self):
        # /********************* Populate the database *******************\
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
        # \----------------------------------------------------------------/


        # /-------------------- User registration -------------------------\
        # Arrange
        request_data = {
            'username': 'testusername',
            'email': 'testemail@mail.ru',
            'password': '123123',
            'repeatedPassword': '123123'
        }

        expected_response_status = status.HTTP_200_OK
        expected_response = {
            'username': 'testusername',
            'email': 'testemail@mail.ru'
        }

        # Act
        response = self.client.post('/api/v0/session/registration/', request_data)

        # Assert
        self.assertEqual(expected_response_status, response.status_code)
        self.assertTrue('token' in response.cookies)
        self.assertEqual(expected_response, response.data)
        # \----------------------------------------------------------------/


        # /----------------- User Login (incorrect data) ------------------\
        # Arange
        request_data = {
            'email': 'incorrectemail@mail.ru',
            'password': 'incorrectpassword'
        }

        expected_response_status = status.HTTP_401_UNAUTHORIZED
        
        # Act
        response = self.client.post('/api/v0/session/login/', request_data)

        # Assert
        self.assertEqual(expected_response_status, response.status_code)
        # \----------------------------------------------------------------/


        # /------------------  User Login (correct data) ------------------\
        # Arrange
        request_data = {
            'email': 'testemail@mail.ru',
            'password': '123123'
        }

        expected_response_status = status.HTTP_200_OK
        expected_response_data = {
            'username': 'testusername',
            'email': 'testemail@mail.ru'
        }

        # Act
        response = self.client.post('/api/v0/session/login/', request_data)

        # Assert
        self.assertEqual(expected_response_status, response.status_code)
        self.assertEqual(expected_response_data, response.data)
        # \----------------------------------------------------------------/


        # /------------------------- Search -------------------------------\
        # Arrange
        search_quote = "Run, Frodo"
        expected_response_status = status.HTTP_200_OK
        expected_response_data = [{
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
        response = self.client.get('/api/v0/movies/quote/', request_data)

        # Assert
        self.assertEqual(expected_response_status, response.status_code)
        self.assertEqual(expected_response_data, response.data)
        # \----------------------------------------------------------------/


        # /--------------------- User history update ----------------------\
        # Arrange
        request_data = {
            "movie_id": "1",
            "quote": search_quote,
            "subtitle_ids": [
                "652",
                "1712"
            ]
        }

        expected_response_status = status.HTTP_200_OK

        # Act
        response = self.client.post('/api/v0/user/testusername/', request_data, format='json')

        # Assert
        self.assertEqual(expected_response_status, response.status_code)
        # \----------------------------------------------------------------/


        # /----------------------- History show ---------------------------\
        # Arrange
        expected_response_status = status.HTTP_200_OK
        expected_response_data = [
            {
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
                        "id": "1712",
                        "quote": "Run, Frodo. Go!",
                        "time": "03:06:04.190000"
                    },
                    {
                        "id": "652",
                        "quote": "Run, Frodo!",
                        "time": "00:56:54.940000"
                    }
                ]
            }
        ]

        # Act
        response = self.client.get('/api/v0/user/testusername/')

        # Assert
        self.assertEqual(expected_response_status, response.status_code)
        self.assertEqual(expected_response_data, response.data)
        # \----------------------------------------------------------------/


    def _cleanup_database(self):
        MovieORM.objects.all().delete()
        User.objects.all().delete()