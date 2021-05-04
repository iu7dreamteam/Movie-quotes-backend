from django.core.management.base import BaseCommand, CommandError

from apps.movie_quotes.infrastructure.django.models.UserProfileORM import User, UserProfileORM
from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.infrastructure.django.models.SubtitleORM import SubtitleORM
from apps.movie_quotes.infrastructure.django.models.MatchORM import MatchORM


class Command(BaseCommand):
    help = "Removes all created records in the database for the movie quotes app"

    def handle(self, *args, **options):
        MovieORM.objects.all().delete()
        User.objects.all().delete()

        movies_count = len(MovieORM.objects.all())
        subtitle_count = len(SubtitleORM.objects.all())
        match_count = len(MatchORM.objects.all())
        users_count = len(User.objects.all())

        self.stdout.write("movies remains:    " + str(movies_count))
        self.stdout.write("subtitles remains: " + str(subtitle_count))
        self.stdout.write("matches remains:   " + str(match_count))
        self.stdout.write("users remains:     " + str(users_count))
