from django.core.management.base import BaseCommand, CommandError

from apps.movie_quotes.utility.subtitle_parser import SubtitleParser

from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo, MatchORM, Match
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM, Movie
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo, SubtitleORM, Subtitle
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo, UserProfileORM, UserProfile, User


class Command(BaseCommand):
    help = 'Populates the database for movie quotes application'

    def handle(self, *args, **options):
        movie_orm_lotr = MovieORM.objects.create(
            title='Lord of the Rings',
            year=2001,
            director='Peter Jackson',
            poster_url='https://someurl.ru',
            video_url='http://videourl.com'
        )
        movie_lotr = MovieRepo().save(movie_orm_lotr)

        # parse subtitles
        subtitle_repo = SubtitleRepo()
        subtitles_lotr = SubtitleParser.parse('./apps/movie_quotes/management/commands/res/LOTR.ru.srt')
        for sub in subtitles_lotr:
            sub.movie = movie_lotr
            subtitle_repo.save(sub)

        self.stdout.write(f'Added {len(subtitles_lotr)} subtitles for movie {movie_lotr.title}')
