from django.core.management.base import BaseCommand

from apps.movie_quotes.utility.subtitle_parser import SubtitleParser

from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM, Movie
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo, Subtitle

import os


class Command(BaseCommand):
    help = "Populates the database for movie quotes application " +\
           " with next content: \n\n" +\
           " 1) Movie #1: Lord of the Rings \n" + \
           " 2) Subtitles for movie #1"

    def handle(self, *args, **options):
        movie_orm_lotr = MovieORM.objects.create(
            title='Lord of the Rings',
            year=2001,
            director='Peter Jackson',
            poster_url='https://someurl.ru',
            video_url='http://videourl.com'
        )
        movie_lotr = MovieRepo().save(movie_orm_lotr)

        subtitle_repo = SubtitleRepo()
        subtitles_lotr = SubtitleParser.parse(os.path.dirname(__file__) + '/res/LOTR.ru.srt')
        for sub in subtitles_lotr:
            sub.movie = movie_lotr
            subtitle_repo.save(sub)

        self.stdout.write(f'Added {len(subtitles_lotr)} subtitles for movie {movie_lotr.title}')
