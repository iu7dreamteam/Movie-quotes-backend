from django.core.management.base import BaseCommand

import os

from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, Movie
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo, Subtitle
from apps.movie_quotes.utility.subtitle_parser import SubtitleParser


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.HOST = 'http://movie-quotes.ru'
        self.STATIC_PATH = '/var/www/movie_quotes.ru/static/' 

        self.movie_repo = MovieRepo()
        self.subtitle_repo = SubtitleRepo()

    def handle(self, *args, **options):
        self.add_the_lord_of_the_rings_2001()
        self.add_the_godfather_1972()
        self.add_forrest_gump_1994()

    def add_the_lord_of_the_rings_2001(self):
        movie_the_lord_of_the_rings_2001 = Movie(
            title='The Lord of The Rings',
            year=2001,
            director='Peter Jackson',
            poster_url=self.HOST + self.STATIC_PATH + 'the_lord_of_the_rings_2001/poster.jpg',
            video_url=self.HOST + self.STATIC_PATH + 'the_lord_of_the_rings_2001/movie.mp4'
        )

        movie_the_lord_of_the_rings_2001 = self.movie_repo.save(movie_the_lord_of_the_rings_2001)
        subtitles = SubtitleParser.parse(self.STATIC_PATH + 'the_lord_of_the_rings_2001/sub.rus.srt')

        for sub in subtitles:
            sub.movie = movie_the_lord_of_the_rings_2001
            self.subtitle_repo.save(sub)

        self._log(movie_the_lord_of_the_rings_2001, len(subtitles))

    def add_the_godfather_1972(self):
        movie_the_godfather_1972 = Movie(
            title='The Godfather',
            year=1972,
            director='Francis Ford Coppola',
            poster_url=self.HOST + self.STATIC_PATH + 'the_godfather_1972/poster.jpg',
            video_url=self.HOST + self.STATIC_PATH + 'the_godfather_1972/movie.mp4'
        )

        movie_the_godfather_1972 = self.movie_repo.save(movie_the_godfather_1972)
        subtitles_pt1 = SubtitleParser.parse(self.STATIC_PATH + 'the_godfather_1972/sub_pt1.rus.srt')
        subtitles_pt2 = SubtitleParser.parse(self.STATIC_PATH + 'the_godfather_1972/sub_pt2.rus.srt')
        subtitles = subtitles_pt1 + subtitles_pt2

        for sub in subtitles:
            sub.movie = movie_the_godfather_1972
            self.subtitle_repo.save(sub)

        self._log(movie_the_godfather_1972, len(subtitles))

    def add_forrest_gump_1994(self):
        movie_forrest_gump_1994 = Movie(
            title='Forrest Gump',
            year=1994,
            director='Robert Zemeckis',
            poster_url=self.HOST + self.STATIC_PATH + 'forrest_gump_1994/poster.jpg',
            video_url=self.HOST + self.STATIC_PATH + 'forrest_gump_1994/movie.mp4'
        )

        movie_forrest_gump_1994 = self.movie_repo.save(movie_forrest_gump_1994)
        subtitles = SubtitleParser.parse(self.STATIC_PATH + 'forrest_gump_1994/sub.rus.srt')

        for sub in subtitles:
            sub.movie = movie_forrest_gump_1994
            self.subtitle_repo.save(sub)

        self._log(movie_forrest_gump_1994, len(subtitles))

    def _log(self, movie, subtitles_count):
        self.stdout.write('Added Movie:')
        self.stdout.write(
            f'\t{movie.title}\n' +
            f'\t{movie.year}\n' +
            f'\t{movie.director}\n' +
            f'\t{movie.poster_url}\n' +
            f'\t{movie.video_url}\n'
        )
        self.stdout.write(f'\tsubtitles count {subtitles_count}')
        self.stdout.write('\n')
