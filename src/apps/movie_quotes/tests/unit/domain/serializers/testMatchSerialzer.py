from django.test import TestCase

from apps.movie_quotes.domain.serializers.MatchSerializer import MatchSerializer
from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo, MatchORM
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo, SubtitleORM
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo, UserProfile, User

from testfixtures import compare

from datetime import time


class TestMatchSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        movie_orm_1 = MovieORM.objects.create(
            title='bomonka1', year=2001, director='me',
            poster_url='https://bmstu.ru',video_url='https://bmstu.ru/poster.png'
        )

        subtitle_orm1 = SubtitleORM.objects.create(quote = "Monday is a bad day!!!",
                                                   start_time = time(hour=0, minute=0, second=37, microsecond=673000),
                                                   end_time = time(hour=0, minute=0, second=39, microsecond=673000),
                                                   movie = movie_orm_1)
        subtitle_orm2 = SubtitleORM.objects.create(quote = "Also Monday is a good day",
                                                   start_time = time(hour=0, minute=1, second=37, microsecond=673000),
                                                   end_time = time(hour=0, minute=0, second=59, microsecond=673001),
                                                   movie = movie_orm_1)

        cls.movie_1 = MovieRepo().get(movie_orm_1.id)
        cls.sub_1 = SubtitleRepo().get(subtitle_orm1.id)
        cls.sub_2 = SubtitleRepo().get(subtitle_orm2.id)

        cls.match = Match(
            quote='test quote',
            movie=cls.movie_1,
            subtitles=[cls.sub_1, cls.sub_2]
        )

        user_orm = User.objects.create(username='testuser', email='test@mail.ru', password='123')
        cls.user_profile = UserProfileRepo().get(user_orm.id)

    def setUp(self):
        pass

    def test__serialize_match(self):
        # Arrange
        expected_json = '{"quote": "test quote", "movie": {"id": "1", "title": "bomonka1", \
"year": "2001", "director": "me", \
"poster": "https://bmstu.ru", "url": "https://bmstu.ru/poster.png"}, \
"quotes": [{"id": "1", "quote": "Monday is a bad day!!!", "time": "00:00:37.673000"}, \
{"id": "2", "quote": "Also Monday is a good day", "time": "00:01:37.673000"}]}'

        # Act
        match_serializer = MatchSerializer()
        actual_json = match_serializer.serialize(self.match)

        # Assert
        compare(expected_json, actual_json)


    def test__deserialize_match(self):
        # Arrange
        expected_match = Match(quote='Monday', movie=self.movie_1, subtitles=[self.sub_1, self.sub_2])

        match_json = f'{{"quote": "Monday", "movie_id": "{self.movie_1.id}", "subtitles": [\
{{ "id": "{self.sub_1.id}" }}, {{ "id": "{self.sub_2.id}" }} ]}}'

        # Act
        match_serializer = MatchSerializer()
        actual_match = match_serializer.deserialize(match_json)

        actual_match.movie = MovieRepo().get(actual_match.movie.id)
        actual_match.subtitles = [SubtitleRepo().get(sub.id) for sub in actual_match.subtitles]

        # Assert
        compare(expected_match, actual_match)
