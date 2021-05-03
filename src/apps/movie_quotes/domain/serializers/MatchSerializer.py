from apps.movie_quotes.domain.entities.Match import Match

from .MovieSerializer import MovieSerializer
from .SubtitleSerializer import SubtitleSerializer

import json

# === Класс представления для конвертации из/в формат словаря (json) экземпляра Match ===

class MatchSerializer:
    # **serialize** - конвертация в json
    def serialize(self, match: Match):
        json_match = self.Encoder().encode(match)
        return json_match

    # **deserialize** - конвертация из json в экземпляр Match
    def deserialize(self, json_match) -> Match:
        dictionary = json.loads(json_match)

        movie_serializer = MovieSerializer()
        subtitle_serializer = SubtitleSerializer()

        movie = {
            'id': dictionary['movie_id']
        }

        movie = movie_serializer.deserialize(movie)

        subtitles = []
        for sub in dictionary['subtitles']:
            subtitle_entity = subtitle_serializer.deserealize(sub)
            subtitles.append(subtitle_entity)

        match = Match(
            quote=dictionary['quote'],
            movie=movie,
            subtitles=subtitles
        )

        return match

    # === Вспомогательный класс конвертации, наследующий методы json.JSONEncoder ===

    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Match):
                return o.to_dict()
