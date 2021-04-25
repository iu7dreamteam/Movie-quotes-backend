from django.db import models

from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.infrastructure.django.models.SubtitleORM import SubtitleORM
from apps.movie_quotes.infrastructure.django.models.UserProfileORM import UserProfileORM


class MatchORM(models.Model):
    class Meta:
        app_label = 'movie_quotes'

    movie = models.ForeignKey(MovieORM, null=False, on_delete=models.CASCADE)
    subtitles = models.ManyToManyField(SubtitleORM)
    user_profile = models.ForeignKey(UserProfileORM, on_delete=models.CASCADE)
