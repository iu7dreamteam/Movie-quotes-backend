from django.test import TestCase

from apps.movie_quotes.domain.repositories.MovieRepo import MovieORM, Movie, MovieRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleORM, SubtitleRepo, Subtitle
from apps.movie_quotes.domain.repositories.MatchRepo import Match, MatchORM, MatchRepo

from datetime import datetime
from testfixtures import compare


class TestMovie(TestCase):
    @classmethod
    def setUpTestData(cls):
        movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        sub_orm_1_movie_1 = SubtitleORM.objects.create(
            quote='Such a nice weather',
            start_time=datetime.now(),
            end_time=datetime.now(),
            movie=movie_orm_1
        )
        
        sub_orm_2_movie_1 = SubtitleORM.objects.create(
            quote='There are lots of misspelling errrorrs',
            start_time=datetime.now(),
            end_time=datetime.now(),
            movie=movie_orm_1
        )

        sub_orm_1_movie_2 = SubtitleORM.objects.create(
            quote='Static variable as local persist...',
            start_time=datetime.now(),
            end_time=datetime.now(),
            movie=movie_orm_1
        )

        cls.movie_1 = MovieRepo().get(movie_orm_1.id)
        cls.sub_1_movie_1 = SubtitleRepo().get(sub_orm_1_movie_1.id)
        cls.sub_2_movie_1 = SubtitleRepo().get(sub_orm_2_movie_1.id)

    
    def setUp(self):
        pass


    # Unfinished test
    def test__to_dict(self):
        match = Match(
            movie=self.movie_1,
            subtitles=[self.sub_1_movie_1, self.sub_2_movie_1]
        )
        
        match_dict = match.to_dict()

