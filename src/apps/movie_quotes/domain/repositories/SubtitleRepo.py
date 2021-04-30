from apps.movie_quotes.infrastructure.django.models.SubtitleORM import SubtitleORM
from apps.movie_quotes.domain.entities.Subtitle import Subtitle
from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo
from apps.movie_quotes.utility.helpers import set_if_not_none

from typing import List

from django.core.exceptions import ObjectDoesNotExist


class SubtitleRepo:
    def save(self, subtitle: Subtitle) -> Subtitle:
        if subtitle.id is None:
            saved_subtitle = self._create(subtitle)
        else:
            try:
                subtitle_orm = SubtitleORM.objects.get(pk=subtitle.id)
                subtitle_orm.quote = set_if_not_none(subtitle_orm.quote, subtitle.quote)
                subtitle_orm.start_time = set_if_not_none(subtitle_orm.start_time, subtitle.start_time)
                subtitle_orm.end_time = set_if_not_none(subtitle_orm.end_time, subtitle_orm.end_time)

                if subtitle.movie is not None:
                    movie_repo = MovieRepo()
                    movie_orm = movie_repo.save(subtitle.movie)
                    subtitle_orm.movie = MovieRepo.Mapper.from_domain(movie_orm)

                subtitle_orm.save()

                saved_subtitle = self.Mapper.to_domain(subtitle_orm)
            except ObjectDoesNotExist:
                saved_subtitle = self._create(subtitle)

        return saved_subtitle

    def delete(self, id):
        subtitle_orm = SubtitleORM.objects.get(id = id)
        subtitle_orm.delete()

    def get(self, id) -> Subtitle:
        subtitle_orm = SubtitleORM.objects.get(id = id)
        return self.Mapper.to_domain(subtitle_orm)

    def find_by_quote(self, quote: str) -> List[Subtitle]:
        subtitles_orm = SubtitleORM.objects.filter(quote__icontains=quote)

        subtitles = []

        for subtitle_orm in subtitles_orm:
            subtitles.append(self.Mapper.to_domain(subtitle_orm))

        return subtitles

    def find_by_quote_ordered_by_movie(self, quote: str) -> List[Subtitle]:
        subtitles_orm = SubtitleORM.objects.filter(quote__icontains=quote)
        subtitles_orm.order_by('movie')

        subtitles = []

        for subtitle_orm in subtitles_orm:
            subtitles.append(self.Mapper.to_domain(subtitle_orm))

        return subtitles

    def _create(self, subtitle: Subtitle) -> Subtitle:
        movie = MovieRepo().save(subtitle.movie)

        subtitle_orm = SubtitleORM.objects.create(
            quote=subtitle.quote,
            start_time=subtitle.start_time,
            end_time=subtitle.end_time,
            movie=MovieRepo.Mapper.from_domain(movie)
        )

        return self.Mapper.to_domain(subtitle_orm)


    class Mapper:
        @staticmethod
        def to_domain(subtitle: SubtitleORM) -> Subtitle:
            return Subtitle(
                id=subtitle.id, quote=subtitle.quote,
                start_time=subtitle.start_time,
                end_time=subtitle.end_time,
                movie=MovieRepo.Mapper.to_domain(subtitle.movie)
            )

        @staticmethod
        def from_domain(subtitle: Subtitle) -> SubtitleORM:
            """
            Subtitle is immutable object. It should't be changed in domain logic at all.
            Thus we can provide mapping from domain object to ORM object just by
            returning it's existing ORM instance by primary key.
            """
            return SubtitleORM.objects.get(pk=subtitle.id)
