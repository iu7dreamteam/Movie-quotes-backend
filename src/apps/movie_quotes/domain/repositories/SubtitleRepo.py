from apps.movie_quotes.infrastructure.django.models.SubtitleORM import SubtitleORM
from apps.movie_quotes.domain.entities.Subtitle import Subtitle
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo
from typing import List

class SubtitleRepo:
    def transform(self, subtitle_orm: SubtitleORM) -> Subtitle:
        return Subtitle(id = subtitle_orm.id, quote = subtitle_orm.quote,
                        start_time = subtitle_orm.start_time,
                        end_time = subtitle_orm.end_time,
                        movie = MovieRepo().transform(subtitle_orm.movie))

    def create(self, subtitle):
        movie_orm = MovieRepo().find_first(subtitle.movie)

        if movie_orm is None:
            movie_orm = MovieRepo().create(subtitle.movie)

        subtitle_orm = SubtitleORM.objects.create(quote = subtitle.quote,
                                                  start_time = subtitle.start_time,
                                                  end_time = subtitle.end_time,
                                                  movie = movie_orm)
        return subtitle_orm

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

    def find_by_quote_ordered_by_movie(self, quote: str) -> List[Subtitle]:
        subtitles_orm = SubtitleORM.objects.filter(quote__icontains=quote)
        subtitles_orm.order_by('movie')

        subtitles = []

        for subtitle_orm in subtitles_orm:
            subtitles.append(self.transform(subtitle_orm))

        return subtitles


    class Mapper:
        @staticmethod
        def from_domain(subtitle: Subtitle) -> SubtitleORM:
            """
            Subtitles is immutable object. It should't be changed in domain logic at all.
            Thus we can provide mapping from domain object to ORM object just by
            returning it's existing ORM instance by primary key.
            """
            return SubtitleORM.objects.get(pk=subtitle.id)
