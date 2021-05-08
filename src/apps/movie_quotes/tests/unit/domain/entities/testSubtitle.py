from django.test import TestCase

from apps.movie_quotes.domain.repositories.MovieRepo import MovieORM, Movie, MovieRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleORM, Subtitle, SubtitleRepo

from testfixtures import compare
from datetime import time, datetime


class TestSubtitle(TestCase):
    @classmethod
    def setUpTestData(cls):
        movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )


        sub_orm_1_movie_1 = SubtitleORM.objects.create(
            quote='Such a nice weather',
            start_time=time(hour=0, minute=0, second=37, microsecond=673000),
            end_time=datetime.now(),
            movie=movie_orm_1
        )
        
        cls.movie_1 = MovieRepo().get(movie_orm_1.id)
        cls.sub_1 = SubtitleRepo().get(sub_orm_1_movie_1.id)


    def setUp(self):
        pass


    def test__to_dict(self):
        expected_dict = {
            'id': str(self.sub_1.id),
            'quote' : self.sub_1.quote,
            'time': "00:00:37.673000"
        }

        actual_dict = self.sub_1.to_dict()

        compare(expected_dict, actual_dict)
