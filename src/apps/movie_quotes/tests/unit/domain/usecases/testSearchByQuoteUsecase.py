from django.test import TestCase
from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.infrastructure.django.models.SubtitleORM import SubtitleORM
from apps.movie_quotes.infrastructure.django.models.UserProfileORM import UserProfileORM, User

from apps.movie_quotes.domain.usecases.SearchByQuoteUsecase import SearchByQuoteUsecase

from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo

from apps.movie_quotes.domain.entities.Match import Match

from datetime import datetime, time
from testfixtures import compare


class TestSearchByQuoteUsecase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Movies
        cls.movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        cls.movie_orm_2 = MovieORM.objects.create(
            title='bomonka2', year=1000, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        cls.movie_orm_3 = MovieORM.objects.create(
            title='bomonka3', year=3000, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        cls.movie_1 = MovieRepo().get(cls.movie_orm_1.id)
        cls.movie_2 = MovieRepo().get(cls.movie_orm_2.id)
        cls.movie_3 = MovieRepo().get(cls.movie_orm_3.id)
        

        # Subs for movie №1
        cls.sub_orm_1_movie_1 = SubtitleORM.objects.create(
            quote="Friend! Hello! .... Bruh!? (hello: 1/3)",
            start_time=time(hour=0, minute=0, second=34, microsecond=420000),
            end_time=time(hour=0, minute=0, second=37,microsecond=420000),
            movie=cls.movie_orm_1
        )

        cls.sub_orm_2_movie_1 = SubtitleORM.objects.create(
            quote="Oh God, when this project will be done :( ... (God: 1/2)",
            start_time=time(hour=0, minute=0, second=34, microsecond=420000),
            end_time=time(hour=0, minute=0, second=37,microsecond=420000),
            movie=cls.movie_orm_1
        )

        cls.sub_orm_3_movie_1 = SubtitleORM.objects.create(
            quote="Hello, mr. Rossinsky! mr Saliery sends his regards (hello: 2/3)",
            start_time=time(hour=0, minute=0, second=34, microsecond=420000),
            end_time=time(hour=0, minute=0, second=37,microsecond=420000),
            movie=cls.movie_orm_1
        )

        # subs for movie №2
        cls.sub_orm_4_movie_2 = SubtitleORM.objects.create(
            quote="God bles aMuuuuuuuuuurica. This is the state of fredom. (God: 2/2)",
            start_time=time(hour=0, minute=0, second=34, microsecond=420000),
            end_time=time(hour=0, minute=0, second=37,microsecond=420000),
            movie=cls.movie_orm_2
        )

        cls.sub_orm_5_movie_2 = SubtitleORM.objects.create(
            quote="Test Quote. Hello, another test (hello: 3/3)",
            start_time=time(hour=0, minute=0, second=34, microsecond=420000),
            end_time=time(hour=0, minute=0, second=37,microsecond=420000),
            movie=cls.movie_orm_2
        )

        cls.sub_orm_6_movie_2 = SubtitleORM.objects.create(
            quote="But who is Joe Biden???",
            start_time=time(hour=0, minute=0, second=34, microsecond=420000),
            end_time=time(hour=0, minute=0, second=37,microsecond=420000),
            movie=cls.movie_orm_2
        )

        cls.sub_1_movie_1 = SubtitleRepo().get(cls.sub_orm_1_movie_1.id)
        cls.sub_2_movie_1 = SubtitleRepo().get(cls.sub_orm_2_movie_1.id)
        cls.sub_3_movie_1 = SubtitleRepo().get(cls.sub_orm_3_movie_1.id)

        cls.sub_4_movie_2 = SubtitleRepo().get(cls.sub_orm_4_movie_2.id)
        cls.sub_5_movie_2 = SubtitleRepo().get(cls.sub_orm_5_movie_2.id)
        cls.sub_6_movie_2 = SubtitleRepo().get(cls.sub_orm_6_movie_2.id)


    def setUp(self):
        pass


    def test__execute__quote_Hello(self):
        # Arrange
        quote = "Hello"

        expected_matches= [
            Match(
                movie=self.movie_1,
                subtitles=[
                    self.sub_1_movie_1,
                    self.sub_3_movie_1
                ]
            ),

            Match(
                movie=self.movie_2,
                subtitles=[
                    self.sub_5_movie_2
                ]
            )
        ]   

        # Act
        match_repo = MatchRepo()
        subtitle_repo = SubtitleRepo()
        usecase = SearchByQuoteUsecase(match_repo, subtitle_repo, quote)
        actual_matches = usecase.execute()

        # Assert
        compare(expected_matches, actual_matches)


    def test__execute__quote_God(self):
        # Arrange
        quote = "God"

        expected_matches= [
            Match(
                movie=self.movie_1,
                subtitles=[
                    self.sub_2_movie_1
                ]
            ),

            Match(
                movie=self.movie_2,
                subtitles=[
                    self.sub_4_movie_2
                ]
            )
        ]   

        # Act
        match_repo = MatchRepo()
        subtitle_repo = SubtitleRepo()
        usecase = SearchByQuoteUsecase(match_repo, subtitle_repo, quote)
        actual_matches = usecase.execute()

        # Assert
        compare(expected_matches, actual_matches)


    def test__execute__no_matches(self):
        # Arrange
        quote = "This qoute exists nowhere"

        expected_matches = []

        # Act
        match_repo = MatchRepo()
        subtitle_repo = SubtitleRepo()
        usecase = SearchByQuoteUsecase(match_repo, subtitle_repo, quote)
        actual_matches = usecase.execute()

        # Assert
        self.assertEqual(expected_matches, actual_matches)


    def test__execute__one_subtitle(self):
        # Arrange
        quote = "Joe Biden"

        expected_matches = [
            Match(
                movie=self.movie_2,
                subtitles=[
                    self.sub_6_movie_2
                ]
            )
        ]

        # Act
        match_repo = MatchRepo()
        subtitle_repo = SubtitleRepo()
        usecase = SearchByQuoteUsecase(match_repo, subtitle_repo, quote)
        actual_matches = usecase.execute()

        # Assert
        compare(expected_matches, actual_matches)
