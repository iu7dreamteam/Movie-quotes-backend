from django.db import models
from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM

class SubtitleORM(models.Model):
    class Meta:
        app_label = 'movie_quotes'

    quote = models.CharField(max_length = 500, db_index = True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    movie = models.ForeignKey(MovieORM, on_delete=models.CASCADE)
