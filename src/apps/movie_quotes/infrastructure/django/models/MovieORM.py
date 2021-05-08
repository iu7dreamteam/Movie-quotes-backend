from django.db import models

# === Модель (таблица) фильмов, среди которых осуществляется поиск ===

class MovieORM(models.Model):
    class Meta:
        app_label = 'movie_quotes'

    """
    Модель MovieORM описывает фильм и содержит следующие поля:
    
    - title - название фильма
    
    - year - год выпуска фильма
    
    - director - имя режиссера
    
    - poster_url - путь к постеру фильма
    
    - video_url - путь к фильму
    """

    title = models.CharField(max_length=180)
    year = models.IntegerField(default=1890)
    director = models.CharField(max_length=180)
    poster_url = models.URLField(max_length = 500)
    video_url = models.URLField(max_length = 500)
