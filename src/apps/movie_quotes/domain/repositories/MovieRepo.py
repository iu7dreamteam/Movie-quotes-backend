from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.domain.entities.Movie import Movie
from apps.movie_quotes.utility.helpers import set_if_not_none

from django.core.exceptions import ObjectDoesNotExist

# === Класс репозиторий фильмов ===

class MovieRepo:
    # **save** - сохранение фильма в БД
    def save(self, movie: Movie) -> Movie:
        if movie.id is None:
            saved_movie = self._create(movie)
        else:
            try:
                movie_orm = MovieORM.objects.get(pk=movie.id)
                movie_orm.title = set_if_not_none(movie_orm.title, movie.title)
                movie_orm.director = set_if_not_none(movie_orm.director, movie.director)
                movie_orm.year = set_if_not_none(movie_orm.year, movie.year)
                movie_orm.poster_url = set_if_not_none(movie_orm.poster_url, movie.poster_url)
                movie_orm.video_url = set_if_not_none(movie_orm.video_url, movie.video_url)

                movie_orm.save()

                saved_movie = self.Mapper.to_domain(movie_orm)
            except ObjectDoesNotExist:
                saved_movie = self._create(movie)

        return saved_movie

    # **get** - получение фильма по идентификатору фильма
    def get(self, id) -> Movie:
        movie_orm = MovieORM.objects.get(id = id)
        return self.Mapper.to_domain(movie_orm)

    # **delete** - удаление фильма по идентификатору фильма
    def delete(self, id):
        movie_orm = MovieORM.objects.get(id = id)
        movie_orm.delete()

    # **find_first** - нахождение первого фильма, удовлетворяющего условиям выборки
    def find_first(self, movie) -> MovieORM:
        return MovieORM.objects.all().filter(title = movie.title, director = movie.director,
                                             year = movie.year, poster_url = movie.poster_url,
                                             video_url = movie.video_url).first()

    # **_create** - создание фильма
    def _create(self, movie: Movie) -> Movie:
        movie_orm = MovieORM.objects.create(
            title=movie.title,
            director=movie.director,
            year=movie.year,
            poster_url=movie.poster_url,
            video_url=movie.video_url
        )

        return self.Mapper.to_domain(movie_orm)

    # === Класс переконвертации из/в модель БД ===

    class Mapper:
        @staticmethod
        def to_domain(movie: MovieORM) -> Movie:
            return Movie(
                id=movie.id, title=movie.title, director=movie.director,
                year=movie.year, poster_url=movie.poster_url,
                video_url=movie.video_url
            )

        @staticmethod
        def from_domain(movie: Movie) -> MovieORM:
            """
            Movie is immutable object at least for now.
            Thus we can provide mapping from domain object to ORM object just by
            returning it's existing ORM instance by primary key.
            """
            return MovieORM.objects.get(pk=movie.id)
