from django.test import TestCase
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo, User

from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.entities.Movie import Movie
from apps.movie_quotes.domain.entities.Subtitle import Subtitle
from apps.movie_quotes.domain.entities.UserProfile import UserProfile

from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.infrastructure.django.models.SubtitleORM import SubtitleORM
from apps.movie_quotes.infrastructure.django.models.MatchORM import MatchORM
from apps.movie_quotes.infrastructure.django.models.UserProfileORM import UserProfileORM

from datetime import datetime, time
from testfixtures import compare


class TestMatchRepo(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser', email='test@mail.ru', password='123123'
        )

        cls.user_profile_orm = UserProfileORM.objects.get(user=cls.user)  

        cls.movie_orm = MovieORM.objects.create(
            title='bomonka', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        cls.sub_orm_1 = SubtitleORM.objects.create(
            quote="Test Quote #1 ...",
            start_time=time(hour=0, minute=0, second=34, microsecond=420000),
            end_time=time(hour=0, minute=0, second=37,microsecond=420000),
            movie=cls.movie_orm
        )

        cls.sub_orm_2 = SubtitleORM.objects.create(
            quote="Test Quote #2 ...",
            start_time=time(hour=0, minute=1, second=34,microsecond=420000),
            end_time=time(hour=0, minute=1, second=37, microsecond=420000),
            movie=cls.movie_orm
        )

        cls.user_profile = UserProfileRepo().get(cls.user.id)
        cls.movie = MovieRepo().get(cls.movie_orm.id)
        cls.sub_1 = SubtitleRepo().get(cls.sub_orm_1.id)
        cls.sub_2 = SubtitleRepo().get(cls.sub_orm_2.id)
        
    def setUp(self):
        pass


    def test__Mapper__to_domain(self):
       # Arrange
        match_orm = MatchORM.objects.create(
            movie=self.movie_orm,
            user_profile=self.user_profile_orm
        )
        match_orm.subtitles.set([self.sub_orm_1, self.sub_orm_2])
        match_orm.save()

        expected_match = Match(
            id=match_orm.id,
            user_profile=self.user_profile,
            movie=self.movie,
            subtitles=[self.sub_1, self.sub_2]
        )

        # Act
        actual_match = MatchRepo().Mapper.to_domain(match_orm)

        # Assert
        compare(expected_match, actual_match)


    def test__Mapper__from_domain(self):
        # Arrange
        expected_match_orm = MatchORM.objects.create(
            movie=self.movie_orm,
            user_profile=self.user_profile_orm
        )
        expected_match_orm.subtitles.set([self.sub_orm_1, self.sub_orm_2])
        expected_match_orm.save()

        match_domain = Match(
            id=1, 
            user_profile=self.user_profile,
            movie=self.movie, 
            subtitles=[self.sub_1, self.sub_2]
        )

        # Act
        actual_match_orm = MatchRepo().Mapper.from_domain(match_domain)

        # Assert
        compare(expected_match_orm, actual_match_orm)


    def test__filter_by_user(self):
        # Arrange
        _user1 = User.objects.create(username='first', email='test1@mail.com', password='123')
        _user2 = User.objects.create(username='second', email='test2@mail.com', password='321')
        _user3 = User.objects.create(username='third', email='test3@mail.com', password='213')

        user1 = UserProfileORM.objects.get(user=_user1)
        user2 = UserProfileORM.objects.get(user=_user2)
        user3 = UserProfileORM.objects.get(user=_user3)

        movie1 = MovieORM.objects.create(title='m1', year=2001, director='dir',
                                         poster_url='http://123', video_url='http://321')

        movie2 = MovieORM.objects.create(title='m2', year=2003, director='dir',
                                         poster_url='http://1234', video_url='http://3214')

        sub1 = SubtitleORM.objects.create(
            quote='test quote',
            start_time=datetime.now(), end_time=datetime.now(),
            movie=movie1
        )

        sub2 = SubtitleORM.objects.create(
            quote='sec quote',
            start_time=datetime.now(), end_time=datetime.now(),
            movie=movie1
        )

        sub3 = SubtitleORM.objects.create(
            quote='third quote',
            start_time=datetime.now(), end_time=datetime.now(),
            movie=movie1
        )

        match1 = MatchORM.objects.create(movie=movie1, user_profile=user1)
        match1.subtitles.set([sub1, sub2])
        match2 = MatchORM.objects.create(movie=movie1, user_profile=user2)
        match2.subtitles.set([sub3])
        match3 = MatchORM.objects.create(movie=movie2, user_profile=user1)
        match3.subtitles.set([sub1, sub2])

        match_repo = MatchRepo()
        expected_query_1 = [
            match_repo.get(id=match1.id),
            match_repo.get(id=match3.id),
        ]

        expected_query_2 = [
            match_repo.get(id=match2.id)
        ]

        # Act
        user_repo = UserProfileRepo()
        user_domain_1 = user_repo.get(user1.id)
        user_domain_2 = user_repo.get(user2.id)

        actual_query_1 = match_repo.filter_by_user(user_profile=user_domain_1)
        actual_query_2 = match_repo.filter_by_user(user_profile=user_domain_2)

        # Assert
        compare(expected_query_1, actual_query_1)
        compare(expected_query_2, actual_query_2)
