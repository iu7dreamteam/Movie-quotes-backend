from django.test import TestCase
from django.contrib.auth.models import User

from apps.movie_quotes.domain.usecases.ShowUserHistoryUsecase import ShowUserHistoryUsecase

from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo, UserProfile, UserProfileORM
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM, Movie
from apps.movie_quotes.domain.repositories.SubtitleRepo import Subtitle, SubtitleORM, SubtitleRepo
from apps.movie_quotes.domain.repositories.MatchRepo import Match, MatchORM, MatchRepo

from datetime import datetime
from testfixtures import compare


class TestShowUserHistoryUsecase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(
            username="testuser",
            email="testemail@mail.ru",
            password="123123"
        )

        user_2 = User.objects.create(
            username="testuser_2",
            email="testemail_2@mail.ru",
            password="12312345"
        )

        user_3 = User.objects.create(
            username="testuser_3",
            email="testemail_4@mail.ru",
            password="1111"
        )

        user_profile_orm_1 = UserProfileORM.objects.get(user=user_1)
        user_profile_orm_2 = UserProfileORM.objects.get(user=user_2)
        user_profile_orm_3 = UserProfileORM.objects.get(user=user_3)

        movie_orm_1 = MovieORM.objects.create(
            title='kino1', year=1,
            director='me', poster_url='123', video_url='123'
        )

        movie_orm_2 = MovieORM.objects.create(
            title='kino2', year=1,
            director='notme', poster_url='1234', video_url='1234'
        )

        movie_orm_3 = MovieORM.objects.create(
            title='kino3', year=1,
            director='notme', poster_url='12345', video_url='12348'
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
            movie=movie_orm_2
        )

        match_1 = MatchORM.objects.create(
            movie=movie_orm_1,
            user_profile=user_profile_orm_1
        )
        match_1.subtitles.set([sub_orm_1_movie_1, sub_orm_2_movie_1])

        match_2 = MatchORM.objects.create(
            movie=movie_orm_2,
            user_profile=user_profile_orm_1
        )
        match_2.subtitles.set([sub_orm_1_movie_2])

        match_3 = MatchORM.objects.create(
            movie=movie_orm_1,
            user_profile=user_profile_orm_2
        )
        match_3.subtitles.set([sub_orm_1_movie_1, sub_orm_2_movie_1])

        cls.user_profile_1 = UserProfileRepo().get(user_1.id)
        cls.user_profile_2 = UserProfileRepo().get(user_2.id)
        cls.user_profile_3 = UserProfileRepo().get(user_3.id)

        cls.movie_1 = MovieRepo().get(movie_orm_1.id)
        cls.movie_2 = MovieRepo().get(movie_orm_2.id)
        cls.movie_3 = MovieRepo().get(movie_orm_3.id)

        cls.sub_1_movie_1 = SubtitleRepo().get(sub_orm_1_movie_1.id)
        cls.sub_2_movie_1 = SubtitleRepo().get(sub_orm_2_movie_1.id)
        cls.sub_1_movie_2 = SubtitleRepo().get(sub_orm_1_movie_2.id)

        cls.match_1 = MatchRepo().get(match_1.id)
        cls.match_2 = MatchRepo().get(match_2.id)
        cls.match_3 = MatchRepo().get(match_3.id)

    def setUp(self):
        pass


    def test__execute(self):
        # Arrange
        expected_matches = [
            self.match_2,
            self.match_1
        ]

        # Act
        usecase = ShowUserHistoryUsecase(
            user_profile=self.user_profile_1,
            user_profile_repo=UserProfileRepo(),
            match_repo=MatchRepo()
        )

        actual_matches = usecase.execute()

        # Assert
        compare(expected_matches, actual_matches)


    def test__execute__empty_history(self):
        # Arrange
        expected_matches = []

        # Act
        usecase = ShowUserHistoryUsecase(
            user_profile=self.user_profile_3,
            user_profile_repo=UserProfileRepo(),
            match_repo=MatchRepo()
        )

        actual_matches = usecase.execute()

        compare(expected_matches, actual_matches)
