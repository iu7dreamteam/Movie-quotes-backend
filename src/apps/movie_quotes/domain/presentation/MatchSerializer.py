from apps.movie_quotes.domain.entities.Match import Match

from .MovieSerializer import MovieSerializer
from .SubtitleSerializer import SubtitleSerializer

import json


class MatchSerializer:
    def serialize(self, match: Match):
        json_match = self.Encoder().encode(match)
        return json_match
    
    def deserialize(self, json_match) -> Match:
        dictionary = json.loads(json_match)

        movie_serializer = MovieSerializer()
        subtitle_serializer = SubtitleSerializer()

        movie = movie_serializer.deserialize(dictionary['movie'])

        subtitles = []
        for sub in dictionary['quotes']:
            subtitle_entity = subtitle_serializer.deserealize(sub)
            subtitles.append(subtitle_entity)

        match = Match(
            movie=movie,
            subtitles=subtitles
        )

        return match

    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Match):
                return o.to_dict()


"""
[
  {
    "movie": {
      "id": 0,
      "title": "string",
      "year": "string",
      "director": "string",
      "poster": "string",
      "url": "string"
    },
    "quotes": [
      {
        "id": 0,
        "quote": "string",
        "time": "string"
      }
    ]
  }
]
"""