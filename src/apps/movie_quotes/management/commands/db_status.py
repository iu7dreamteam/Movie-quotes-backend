from django.core.management.base import BaseCommand, CommandError

from apps.movie_quotes.utility.subtitle_parser import SubtitleParser

from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo, MatchORM, Match
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo, MovieORM, Movie
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo, SubtitleORM, Subtitle
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo, UserProfileORM, UserProfile, User

class Command(BaseCommand):
    help = "Removes all created records in the database for the movie quotes app"

    def handle(self, *args, **options):
        movies_count = len(MovieORM.objects.all())
        subtitle_count = len(SubtitleORM.objects.all())
        match_count = len(MatchORM.objects.all())
        users_count = len(User.objects.all())

        self.stdout.write("movies count:    " + str(movies_count))
        self.stdout.write("subtitles count: " + str(subtitle_count))
        self.stdout.write("matches count:   " + str(match_count))
        self.stdout.write("users count:     " + str(users_count))
