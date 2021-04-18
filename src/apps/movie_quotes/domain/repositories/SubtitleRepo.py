from apps.movie_quotes.infrastructure.django.models.SubtitleORM import SubtitleORM
from apps.movie_quotes.domain.entities.Subtitle import Subtitle
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo
from typing import List

class SubtitleRepo:
    def transform(self, subtitle_orm: SubtitleORM) -> Subtitle:
        movies = []
        for movie_orm in subtitle_orm.movies.all():
            movies.append(MovieRepo().transform(movie_orm))
        return Subtitle(id = subtitle_orm.id, quote = subtitle_orm.quote,
                        start_time = subtitle_orm.start_time,
                        end_time = subtitle_orm.end_time,
                        movies = movies)

    def create(self, subtitle):
        subtitle_orm = SubtitleORM.objects.create(quote = subtitle.quote,
                                                  start_time = subtitle.start_time,
                                                  end_time = subtitle.end_time)

        for movie in subtitle.movies:
            movie_orm = MovieRepo().find_first(movie)

            if movie_orm is None:
                movie_orm = MovieRepo().create(movie)

            subtitle_orm.movies.add(movie_orm)

    def delete(self, id):
        subtitle_orm = SubtitleORM.objects.get(id = id)
        subtitle_orm.delete()

    def get(self, id) -> Subtitle:
        subtitle_orm = SubtitleORM.objects.get(id = id)
        return self.transform(subtitle_orm)

    def find_by_quote(self, quote: str) -> List[Subtitle]:
        subtitles_orm = SubtitleORM.objects.filter(quote__icontains=quote)

        subtitles = []

        for subtitle_orm in subtitles_orm:
            subtitles.append(self.transform(subtitle_orm))

        return subtitles




