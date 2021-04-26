from django.test import TestCase

from apps.movie_quotes.domain.repositories.MovieRepo import MovieORM, Movie, MovieRepo

from testfixtures import compare


class TestMovie(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        cls.movie_1 = MovieRepo().get(cls.movie_orm_1.id)


    def setUp(self):
        pass


    def test__to_dict(self):
        expected_dict = {
            'id': str(self.movie_1.id),
            'title' : 'bomonka1',
            "year": '2001',
            "director": 'me',
            "poster": 'https://bmstu.ru',
            "url": 'https://bmstu.ru/poster.png'
        }

        actual_dict = self.movie_1.to_dict()

        compare(expected_dict, actual_dict)
