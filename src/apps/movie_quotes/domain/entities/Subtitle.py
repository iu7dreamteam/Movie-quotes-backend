from apps.movie_quotes.domain.entities.Movie import Movie

class Subtitle(object):
    def __init__(self, id = None, quote = '', start_time = None, end_time = None, movies = []):
        self._id = id
        self._quote = quote
        self._start_time = start_time
        self._end_time = end_time
        self._movies = movies

    @property
    def id(self):
        return self._id

    @property
    def quote(self):
        return self._quote

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def movies(self):
        return self._movies

    @id.setter
    def id(self, id):
        self._id = id

    @quote.setter
    def quote(self, quote):
        self._quote = quote

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @end_time.setter
    def end_time(self, end_time):
        self._end_time = end_time

    @movies.setter
    def movies(self, movies):
        self._movies = movies

    def add_movie(self, movie):
        self._movies.append(movie)
