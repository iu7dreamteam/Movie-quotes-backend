from django.core.management.base import BaseCommand

import os
import shutil
import urllib.request
from typing import List

from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, Movie
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo, Subtitle
from apps.movie_quotes.utility.subtitle_parser import SubtitleParser


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # pylint: disable-msg=C0103
        self.HOST = 'http://movie-quotes.ru'
        self.STATIC_PATH = '/static/'

        self._movie_repo = MovieRepo()
        self._subtitle_repo = SubtitleRepo()

    def handle(self, *args, **options):
        # pylint: disable-msg=C0103
        # ---------------------- The Lord Of the Rings 2001 ------------------------
        movie_the_lord_of_the_rings_2001 = Movie(
            title='The Lord of The Rings',
            year=2001,
            director='Peter Jackson',
            poster_url=self.HOST + self.STATIC_PATH + 'the_lord_of_the_rings_2001/poster.jpg',
            video_url=self.HOST + self.STATIC_PATH + 'the_lord_of_the_rings_2001/movie.mp4'
        )
        dir_name = 'the_lord_of_the_rings_2001'
        self._populate_movie(movie_the_lord_of_the_rings_2001,
                             dir_name,
                             [self.HOST + self.STATIC_PATH + dir_name +'/' + 'sub.rus.srt'])


        # --------------------------- Forrest Gump 1994 ----------------------------
        movie_forrest_gump_1994 = Movie(
            title='Forrest Gump',
            year=1994,
            director='Robert Zemeckis',
            poster_url=self.HOST + self.STATIC_PATH + 'forrest_gump_1994/poster.jpg',
            video_url=self.HOST + self.STATIC_PATH + 'forrest_gump_1994/movie.mp4'
        )
        dir_name = 'forrest_gump_1994'
        self._populate_movie(movie_forrest_gump_1994,
                             dir_name,
                             [self.HOST + self.STATIC_PATH + dir_name + '/' + 'sub.rus.srt'])


        # --------------------------- The Godfather 1972 ----------------------------
        movie_the_godfather_1972 = Movie(
            title='The Godfather',
            year=1972,
            director='Francis Ford Coppola',
            poster_url=self.HOST + self.STATIC_PATH + 'the_godfather_1972/poster.jpg',
            video_url=self.HOST + self.STATIC_PATH + 'the_godfather_1972/movie.mp4'
        )
        dir_name = 'the_godfather_1972'
        self._populate_movie(movie_the_godfather_1972,
                            dir_name, [
                                self.HOST + self.STATIC_PATH + dir_name + '/' + 'sub_pt1.rus.srt',
                                self.HOST + self.STATIC_PATH + dir_name + '/' + 'sub_pt2.rus.srt'
                            ])


    def _download_files(self, tmp_dirname, urls: list) -> List[str]:
        '''
        Downloads files from given urls into temporary directory tmp_dirname.
        Returns list of filenames, which were download succesfully.
        '''
        downloaded_filepaths = []

        os.mkdir(tmp_dirname)
        self.stdout.write(f'created temporary directory: {tmp_dirname}')

        for url in urls:
            self.stdout.write(f'downloading file: {url} ...')
            filepath = tmp_dirname + '/' + url.split('/')[-1]
            urllib.request.urlretrieve(url, filepath)
            downloaded_filepaths.append(filepath)

        return downloaded_filepaths

    def _read_subtitles(self, movie_dirname, subtitle_files_urls: list) -> List[Subtitle]:
        downloaded_files = self._download_files(movie_dirname, subtitle_files_urls)

        subtitles = []
        for filepath in downloaded_files:
            self.stdout.write(f'reading file with subtitles: {filepath} ...')
            subtitles_part = SubtitleParser.parse(filepath)
            subtitles += subtitles_part

        shutil.rmtree(movie_dirname)
        self.stdout.write(f'deleted temporary directory: {movie_dirname}')

        return subtitles

    def _populate_movie(self, movie, movie_dir_name, subtitle_files_urls):
        movie = self._movie_repo.save(movie)

        subtitles = self._read_subtitles(movie_dir_name, subtitle_files_urls)

        for sub in subtitles:
            sub.movie = movie
            self._subtitle_repo.save(sub)

        self._log(movie, len(subtitles))


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
