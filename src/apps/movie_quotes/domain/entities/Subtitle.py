from apps.movie_quotes.domain.entities.Movie import Movie

# === Модель бизнес-логики для описания субтитра ===

class Subtitle(object):
    def __init__(self, id = None, quote = '', start_time = None, end_time = None, movie = None):
        self._id = id
        self._quote = quote
        self._start_time = start_time
        self._end_time = end_time
        self._movie = movie

    """
    Поля Movie:
    
    - id - идентификатор субтитра
    
    - quote - цитата
    
    - start_time - время, когда цитата начинается в фильме
    
    - end_time - время, когда цитата начинается в фильме
    
    - movie - фильм, к которому относится цитата
    
    """

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
    def movie(self):
        return self._movie

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

    @movie.setter
    def movie(self, movie):
        self._movie = movie

    # Метод переконвертации объекта Subtitle в словарь
    def to_dict(self):
        return {
            "id": str(self.id),
            "quote": self.quote,
            "time": self.start_time.strftime("%H:%M:%S.%f")
        }
