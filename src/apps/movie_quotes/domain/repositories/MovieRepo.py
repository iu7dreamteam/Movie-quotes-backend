from apps.movie_quotes.infrastructure.django.models.MovieORM import MovieORM
from apps.movie_quotes.domain.entities.Movie import Movie

class MovieRepo:
    def transform(self, movie_orm: MovieORM) -> Movie:
        return Movie(id = movie_orm.id, title = movie_orm.title, director = movie_orm.director,
                     year = movie_orm.year, poster_url = movie_orm.poster_url,
                     video_url = movie_orm.video_url)

    def create(self, movie) -> MovieORM:
        return MovieORM.objects.create(title = movie.title, director = movie.director,
                                       year = movie.year, poster_url = movie.poster_url,
                                       video_url = movie.video_url)

    def get(self, id) -> Movie:
        movie_orm = MovieORM.objects.get(id = id)
        return self.transform(movie_orm)

    def delete(self, id):
        movie_orm = MovieORM.objects.get(id = id)
        movie_orm.delete()

    def find_first(self, movie) -> MovieORM:
        return MovieORM.objects.all().filter(title = movie.title, director = movie.director,
                                             year = movie.year, poster_url = movie.poster_url,
                                             video_url = movie.video_url).first()