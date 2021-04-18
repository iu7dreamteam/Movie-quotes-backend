from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.domain.entities.Movie import Movie

class MovieRepo:
    def transform(self, movie_orm: MovieORM) -> Movie:
        return Movie(id = movie_orm.id, name = movie_orm.name,
                     year = movie_orm.year, url = movie_orm.url)

    def create(self, movie) -> MovieORM:
        return MovieORM.objects.create(name = movie.name, year = movie.year, url = movie.url)

    def get(self, id) -> Movie:
        movie_orm = MovieORM.objects.get(id = id)
        return self.transform(movie_orm)

    def delete(self, id):
        movie_orm = MovieORM.objects.get(id = id)
        movie_orm.delete()

    def find_first(self, movie) -> MovieORM:
        return MovieORM.objects.all().filter(name = movie.name,
                                             year = movie.year,
                                             url = movie.url).first()