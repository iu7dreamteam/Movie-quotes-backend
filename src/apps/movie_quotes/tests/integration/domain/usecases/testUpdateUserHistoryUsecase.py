from django.test import TestCase
from django.contrib.auth.models import User

from apps.movie_quotes.domain.usecases.UpdateUserHistoryUsecase import UpdateUserHistoryUsecase

from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo, UserProfile, UserProfileORM
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM, Movie
from apps.movie_quotes.domain.repositories.SubtitleRepo import Subtitle, SubtitleORM, SubtitleRepo
from apps.movie_quotes.domain.repositories.MatchRepo import Match, MatchORM, MatchRepo

from datetime import datetime
from testfixtures import compare


class TestUpdateUserHistoryUsecase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(
            username="testuser",
            email="testemail@mail.ru",
            password="123123"
        )

        movie_orm_1 = MovieORM.objects.create(
            title='kino1', year=1, 
            director='me', poster_url='123', video_url='123'
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

        sub_orm_3_movie_1 = SubtitleORM.objects.create(
            quote='new history match',
            start_time=datetime.now(),
            end_time=datetime.now(),
            movie=movie_orm_1
        )

        cls.user_profile_1 = UserProfileRepo().get(user_1.id)
        cls.movie_1 = MovieRepo().get(movie_orm_1.id)
        cls.sub_1_movie_1 = SubtitleRepo().get(sub_orm_1_movie_1.id)
        cls.sub_2_movie_1 = SubtitleRepo().get(sub_orm_2_movie_1.id)
        cls.sub_3_movie_1 = SubtitleRepo().get(sub_orm_3_movie_1.id)


    def setUp(self):
        pass


    def test__execute__history_empty(self):
        # Arrange
        match_to_save = Match(
            user_profile=self.user_profile_1,
            movie=self.movie_1,
            subtitles=[self.sub_1_movie_1, self.sub_2_movie_1]
        )

        # Act
        usecase = UpdateUserHistoryUsecase(
            user_profile=self.user_profile_1,
            match_to_save=match_to_save,
            match_repo=MatchRepo()
        )

        usecase.execute()

        match_orm = MatchORM.objects.latest('id')
        expected_user_matches = [
            MatchRepo().get(match_orm.id)
        ]

        # Assert
        # retrieve user history
        actual_user_matches = MatchRepo().filter_by_user(self.user_profile_1)

        compare(expected_user_matches, actual_user_matches)


    def test__execute(self):
        # Arrange
        # fill up the history
        match_1 = Match(
            user_profile=self.user_profile_1,
            movie=self.movie_1,
            subtitles=[self.sub_1_movie_1, self.sub_2_movie_1])
        match_1 = MatchRepo().save(match_1)


        match_2 = Match(
            user_profile=self.user_profile_1,
            movie=self.movie_1,
            subtitles=[self.sub_1_movie_1])
        match_2 = MatchRepo().save(match_2)

        # Act
        match_to_save = Match(
            user_profile=self.user_profile_1,
            movie=self.movie_1,
            subtitles=[self.sub_1_movie_1, self.sub_3_movie_1]
        )

        usecase = UpdateUserHistoryUsecase(
            user_profile=self.user_profile_1,
            match_to_save=match_to_save,
            match_repo=MatchRepo()
        )

        usecase.execute()

        latest_match_orm = MatchORM.objects.latest('id')
        expected_user_matches = [
            MatchRepo().get(latest_match_orm.id),
            match_2,
            match_1
        ]

        actual_user_matches = MatchRepo().filter_by_user(self.user_profile_1)

        # Assert
        compare(expected_user_matches, actual_user_matches)
