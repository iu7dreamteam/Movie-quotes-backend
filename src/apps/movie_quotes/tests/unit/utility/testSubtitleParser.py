from django.test import TestCase
from testfixtures import compare

from apps.movie_quotes.domain.entities.Subtitle import Subtitle
from apps.movie_quotes.utility.subtitle_parser import SubtitleParser

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
        actual_subtitles = SubtitleParser.parse('./apps/movie_quotes/tests/unit/utility/res/The_Lord_of_the_Rings(2001).srt')

        # Assert
        compare(actual_subtitles, expected_subtitles)

    def test_parse__lang_ru(self):
        expected_subtitles = [
            Subtitle(
                start_time=time(hour=0, minute=0, second=32, microsecond=560000),
                end_time=time(hour=0, minute=0, second=35, microsecond=470000),
                quote='Мир изменился.'
            ),

            Subtitle(
                start_time=time(hour=0, minute=0, second=35, microsecond=640000),
                end_time=time(hour=0, minute=0, second=38, microsecond=550000),
                quote='Я чувствую это в воде.'
            ),

            Subtitle(
                start_time=time(hour=0, minute=0, second=39, microsecond=280000),
                end_time=time(hour=0, minute=0, second=42, microsecond=80000),
                quote='Я чувствую это в земле.'
            ),
        ]

        # Act
        actual_subtitles = SubtitleParser.parse('./apps/movie_quotes/tests/unit/utility/res/The_Lord_of_the_Rings(2001).ru.srt')

        # Assert
        compare(actual_subtitles, expected_subtitles)

    
    def test_parse__lang_bengal__cleanning_formatting(self):
        expected_subtitles = [
            Subtitle(
                start_time=time(hour=0, minute=0, second=31, microsecond=250000),
                end_time=time(hour=0, minute=0, second=34, microsecond=549000),
                quote='I amar prestar aen.'
            ),

            Subtitle(
                start_time=time(hour=0, minute=0, second=36, microsecond=650000),
                end_time=time(hour=0, minute=0, second=37, microsecond=749000),
                quote='Han mathon ne nen.'
            ),

            Subtitle(
                start_time=time(hour=0, minute=0, second=39, microsecond=950000),
                end_time=time(hour=0, minute=0, second=41, microsecond=549000),
                quote='Han mathon ne chae.'
            ),
        ]

        # Act
        actual_subtitles = SubtitleParser.parse('./apps/movie_quotes/tests/unit/utility/res/The_Lord_of_the_Rings(2001).bengal.colored.srt')

        # Assert
        compare(actual_subtitles, expected_subtitles)

