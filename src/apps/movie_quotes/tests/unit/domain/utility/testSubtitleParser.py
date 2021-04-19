from django.test import TestCase
from testfixtures import compare

from apps.movie_quotes.domain.entities.Subtitle import Subtitle
from apps.movie_quotes.domain.utility.subtitle_parser import SubtitleParser

from datetime import time


class TestSubtitleParser(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_parse__lang_en(self):
        # Arrange
        expected_subtitles = [
            Subtitle(
                start_time=time(hour=0, minute=0, second=34, microsecond=420000),
                end_time=time(hour=0, minute=0, second=37, microsecond=506000),
                quote='The world is changed.'
            ),

            Subtitle(
                start_time=time(hour=0, minute=0, second=37, microsecond=673000),
                end_time=time(hour=0, minute=0, second=40, microsecond=676000),
                quote='I feel it in the water.'
            ),

            Subtitle(
                start_time=time(hour=0, minute=0, second=41, microsecond=427000),
                end_time=time(hour=0, minute=0, second=44, microsecond=346000),
                quote='I feel it in the earth.'
            ),
        ]

        # Act
        actual_subtitles = SubtitleParser.parse('./apps/movie_quotes/tests/unit/domain/utility/res/The_Lord_of_the_Rings(2001).srt')

        # Assert
        compare(actual_subtitles, expected_subtitles)

