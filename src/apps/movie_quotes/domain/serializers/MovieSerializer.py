from apps.movie_quotes.domain.entities.Movie import Movie

import json

# === Класс представления для конвертации из/в формат словаря (json) экземпляра Movie ===

class MovieSerializer:
    # **serialize** - конвертация в json
    def serialize(self, movie: Movie):
        json_movie = self.Encoder().encode(movie)
        return json_movie

    # **deserialize** - конвертация из json в экземпляр Movie
    def deserialize(self, serialized) -> Movie:
        if isinstance(serialized, str):
            serialized = json.loads(serialized)
        return self._parse_dictionary(serialized)

    # **_parse_dictionary** - парсер словаря и запись полей словаря в экземпляр Movie
    def _parse_dictionary(self, dictionary) -> Movie:
        movie = Movie(id=None, title=None, year=None, director=None,
                      poster_url=None, video_url=None)

        if "id" in dictionary:
            movie.id = int(dictionary["id"])
        if "title" in dictionary:
            movie.title = dictionary["title"]
        if "director" in dictionary:
            movie.director = dictionary["director"]
        if "year" in dictionary:
            movie.year = int(dictionary["year"])
        if "poster" in dictionary:
            movie.poster_url = dictionary["poster"]
        if "url" in dictionary:
            movie.video_url = dictionary["url"]

        return movie

    # === Вспомогательный класс конвертации, наследующий методы json.JSONEncoder ===

    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Movie):
                return o.to_dict()
