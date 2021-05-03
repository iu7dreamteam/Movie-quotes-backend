# === Модель бизнес-логики для описания фильма ===

class Movie(object):
    def __init__(self, id = None, title = '', year = 0, director = '', poster_url = '', video_url = ''):
        self._id = id
        self._title = title
        self._year = year
        self._director = director
        self._poster_url = poster_url
        self._video_url = video_url

    """
    Поля Movie:
    
    - id - идентификатор фильма
    
    - title - название фильма
    
    - year - год выпуска фильма
    
    - director - имя режиссера
    
    - poster_url - путь к постеру фильма
    
    - video_url - путь к фильму
    
    """

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def year(self):
        return self._year

    @property
    def director(self):
        return self._director

    @property
    def poster_url(self):
        return self._poster_url

    @property
    def video_url(self):
        return self._video_url

    @id.setter
    def id(self, id):
        self._id = id

    @title.setter
    def title(self, title):
        self._title = title

    @year.setter
    def year(self, year):
        self._year = year

    @director.setter
    def director(self, director):
        self._director = director

    @poster_url.setter
    def poster_url(self, poster_url):
        self._poster_url = poster_url

    @video_url.setter
    def video_url(self, video_url):
        self._video_url = video_url

    # Метод переконвертации объекта Movie в словарь
    def to_dict(self):
        data = {}
        data["id"] = str(self._id)
        data["title"] = self._title
        data["year"] = str(self._year)
        data["director"] = self._director
        data["poster"] = self.poster_url
        data["url"] = self._video_url

        return data
