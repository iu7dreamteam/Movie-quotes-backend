from django.db import models
from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM

# === Модель (таблица) субтитров ===

class SubtitleORM(models.Model):
    class Meta:
        app_label = 'movie_quotes'

    """
    Модель SubtitleORM описывает субтитры и содержит следующие поля:
    
    - quote - цитата
    
    - start_time - время, когда цитата начинается в фильме
    
    - end_time - время, когда цитата начинается в фильме
    
    - movie - фильм, к которому относится цитата
    """

    quote = models.CharField(max_length = 500, db_index = True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    movie = models.ForeignKey(MovieORM, on_delete=models.CASCADE)
