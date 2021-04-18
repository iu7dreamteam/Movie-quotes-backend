from django.db import models

class MovieORM(models.Model):
    name = models.CharField(max_length=180)
    year = models.IntegerField(default=1890)
    url = models.URLField(max_length = 200)