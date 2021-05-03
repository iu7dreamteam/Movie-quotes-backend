from django.db import models

from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.infrastructure.django.models.SubtitleORM import SubtitleORM
from apps.movie_quotes.infrastructure.django.models.UserProfileORM import UserProfileORM

# === Модель (таблица) истории пользователя ===

class MatchORM(models.Model):
    class Meta:
        app_label = 'movie_quotes'

    """
    Модель MatchORM несет информацию об истории пользователя и содержит следующие поля:
    
    - quote - строка запроса, которую ввел пользователь

    - movie - название фильма, который был просмотрен пользователем
    
    - subtitles - субтитры
    
    - user_profile - пользователь
    """

    quote = models.CharField(max_length=200, null=False)
    movie = models.ForeignKey(MovieORM, null=False, on_delete=models.CASCADE)
    subtitles = models.ManyToManyField(SubtitleORM)
    user_profile = models.ForeignKey(UserProfileORM, on_delete=models.CASCADE)
