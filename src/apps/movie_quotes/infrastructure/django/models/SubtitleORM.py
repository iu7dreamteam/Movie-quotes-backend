from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM

class SubtitleORM(models.Model):
    quote = models.CharField(max_length = 500, db_index = True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    movies = models.ManyToManyField(MovieORM)