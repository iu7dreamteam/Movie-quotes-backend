from apps.movie_quotes.domain.entities.Movie import Movie

import json

class MovieSerializer:
    def serialize(self, movie: Movie):
        json_movie = self.Encoder().encode(movie)
        return json_movie

    def deserialize(self, json_movie) -> Movie:
        """
            Movies are immutable for client side.
            Thus, for now, just for speed development we will
            retrive only movie id from received json-movie string,
            and later get complete movie object from repository by
            this id.
        """

        if isinstance(json_movie, dict):
            id = json_movie['id']
        else:                           # Actual json string
            try:
                dictionary = json.loads(json_movie)
                id = dictionary['id']
            except TypeError:
                id = None

        movie = Movie(
            id=id
        )

        return movie

    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Movie):
                return o.to_dict()
