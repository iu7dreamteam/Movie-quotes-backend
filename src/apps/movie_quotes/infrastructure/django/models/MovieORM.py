from django.db import models

class MovieORM(models.Model):
    class Meta:
        app_label = 'movie_quotes'

    title = models.CharField(max_length=180)
    year = models.IntegerField(default=1890)
    director = models.CharField(max_length=180)
    poster_url = models.URLField(max_length = 500)
    video_url = models.URLField(max_length = 500)
