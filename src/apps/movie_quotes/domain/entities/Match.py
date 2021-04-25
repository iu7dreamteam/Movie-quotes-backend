from apps.movie_quotes.domain.entities.Movie import Movie
from apps.movie_quotes.domain.entities.Subtitle import Subtitle


class Match(object):
    def __init__(self, id=None, user_profile=None, movie=None, subtitles=[]):
        self._id = id
        self._user_profile = user_profile
        self._movie = movie
        self._subtitles = subtitles

    @property
    def id(self):
        return self._id

    @property
    def user_profile(self):
        return self._user_profile

    @property
    def movie(self):
        return self._movie

    @property
    def subtitles(self):
        return self._subtitles


    @id.setter
    def id(self, id):
        self._id = id

    @movie.setter
    def movie(self, movie):
        self._movie = movie

    @subtitles.setter
    def subtitles(self, subtitles):
        self._subtitles = subtitles

    
    def append_subtitle(self, subtitle: Subtitle):
        if subtitle.movie.id != self.movie.id:
            raise DifferentMoviesInsertionError(
                f'ids: {movie.id}, {self.movie_id}'
            )

        self.subtitles.append(subtitle)


class DifferentMoviesInsertionError(Exception):
    def __init__(self, message):
        self.message = 'Match can only contain subtitles from one movie' + message
        super().__init__(self.message)
    