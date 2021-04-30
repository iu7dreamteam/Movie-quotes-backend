from django.test import TestCase
from apps.movie_quotes.domain.presentation.SubtitleSerializer import SubtitleSerializer
from apps.movie_quotes.domain.presentation.MovieSerializer import MovieSerializer
from apps.movie_quotes.domain.presentation.MatchSerializer import MatchSerializer

from apps.movie_quotes.domain.repositories.MovieRepo import MovieORM, Movie, MovieRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleORM, Subtitle, SubtitleRepo
from apps.movie_quotes.domain.repositories.MatchRepo import Match, MatchORM, MatchRepo
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfile, UserProfileRepo, User

from datetime import time
from testfixtures import compare


class TestSerializers(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(
            username="testuser",
            email="testemail@mail.ru",
            password="123123"
        )

        cls.movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        cls.sub_orm_1_movie_1 = SubtitleORM.objects.create(
            quote="Friend! Hello! .... Bruh!?",
            start_time=time(hour=0, minute=0, second=34, microsecond=420000),
            end_time=time(hour=0, minute=0, second=37,microsecond=420000),
            movie=cls.movie_orm_1
        )

        cls.sub_orm_2_movie_1 = SubtitleORM.objects.create(
            quote="Hello there. Lets finish this project please!?",
            start_time=time(hour=0, minute=0, second=34, microsecond=420000),
            end_time=time(hour=0, minute=0, second=37,microsecond=420000),
            movie=cls.movie_orm_1
        )

        cls.user_profile_1 = UserProfileRepo().get(user_1.id)
        cls.movie_1 = MovieRepo().get(cls.movie_orm_1.id)
        cls.sub_1 = SubtitleRepo().get(cls.sub_orm_1_movie_1.id)
        cls.sub_2 = SubtitleRepo().get(cls.sub_orm_2_movie_1.id)


    def setUp(self):
        pass

    
    def test__retrieve_subtitle_entity_from_serialized_data(self):
        # Arrange
        expected_subtitle = Subtitle(
            id=self.sub_1.id,
            quote=self.sub_1.quote,
            start_time=self.sub_1.start_time,
            end_time=self.sub_1.end_time,
            movie=self.sub_1.movie
        )

        # Act
        serializer = SubtitleSerializer()
        serialized_sub = serializer.serialize(expected_subtitle)

        deserialized_subtitle = serializer.deserealize(serialized_sub)

        actual_subtitle = SubtitleRepo().get(deserialized_subtitle.id)

        # Assert
        compare(expected_subtitle, actual_subtitle)


    def test__retrieve_movie_entity_from_serialized_data(self):
        # Arrange
        expected_movie = self.movie_1

        # Act
        serializer = MovieSerializer()
        serialized_movie = serializer.serialize(self.movie_1)

        deserialized_movie = serializer.deserialize(serialized_movie)

        actual_movie = MovieRepo().get(deserialized_movie.id)

        # Assert
        compare(expected_movie, actual_movie)


    #def test__serialize_and_deserialize_match(self):
    #    # Arrange
    #    match_to_serialize = Match(
    #        movie=self.movie_1,
    #        subtitles=[self.sub_1, self.sub_2]
    #    )
    #
    #    match_serializer = MatchSerializer()
    #    serialized_match = match_serializer.serialize(match_to_serialize)
    #    deserialized_match = match_serializer.deserialize(serialized_match)
    #
    #    # Post serialization updates
    #    deserialized_match.user_profile = self.user_profile_1
    #    actual_match = MatchRepo().save(deserialized_match)
    #
    #    expected_match = Match(
    #        id=actual_match.id,
    #        user_profile=self.user_profile_1,
    #        movie=self.movie_1,
    #        subtitles=[self.sub_1, self.sub_2]
    #    )
    #
    #    # Assert
    #    compare(actual_match, expected_match)
