from apps.movie_quotes.domain.entities.Movie import Movie
from apps.movie_quotes.domain.entities.Subtitle import Subtitle

# === Модель бизнес-логики для хранения пользовательской истории ===

class Match(object):
    def __init__(self, id=None, quote=None, user_profile=None, movie=None, subtitles=None):
        self._id = id
        self._quote = quote
        self._user_profile = user_profile
        self._movie = movie
        self._subtitles = subtitles

    """
    Поля Match:
    
    - id - идентификатор истории пользователя

    - quote - строка запроса, введенная пользователем
    
    - user_profile - профиль пользователя
    
    - movie - фильм, просмотренный пользователем
    
    - subtitles - субтитры, относящиеся к фильму
    
    """

    @property
    def id(self):           # pylint:disable=duplicate-code
        return self._id

    @property
    def quote(self):        # pylint:disable=duplicate-code
        return self._quote

    @property
    def user_profile(self):
        return self._user_profile

    @property
    def movie(self):
        return self._movie

    @property
    def subtitles(self):
        return self._subtitles


    @user_profile.setter
    def user_profile(self, user_profile):
        self._user_profile = user_profile

    @id.setter              # pylint:disable=duplicate-code
    def id(self, id):
        self._id = id

    @quote.setter           # pylint:disable=duplicate-code
    def quote(self, quote):
        self._quote = quote

    @movie.setter
    def movie(self, movie):
        self._movie = movie

    @subtitles.setter
    def subtitles(self, subtitles):
        self._subtitles = subtitles

    # Метод добавления субтитра в массив субтитров
    def append_subtitle(self, subtitle: Subtitle):
        if subtitle.movie.id != self.movie.id:
            raise DifferentMoviesInsertionError(
                f'ids: {subtitle.movie.id}, {self.movie_id}'
            )

        self.subtitles.append(subtitle)

    # Метод конвертации объекта Match в словарь
    def to_dict(self):
        data = {}
        data["quote"] = self.quote
        data["movie"] = self.movie.to_dict()

        subtitles = []
        for sub in self.subtitles:
            subtitles.append(sub.to_dict())

        data["quotes"] = subtitles

        return data


class DifferentMoviesInsertionError(Exception):
    def __init__(self, message):
        self.message = 'Match can only contain subtitles from one movie' + message
        super().__init__(self.message)
    