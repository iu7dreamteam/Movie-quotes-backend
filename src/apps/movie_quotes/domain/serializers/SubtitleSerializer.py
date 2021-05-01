from apps.movie_quotes.domain.entities.Subtitle import Subtitle

import json


class SubtitleSerializer:
    def serialize(self, subtitle: Subtitle):
        json_subtitle = self.Encoder().encode(subtitle)
        return json_subtitle

    def deserealize(self, serialized) -> Subtitle:
        if isinstance(serialized, str):
            serialized = json.loads(serialized)
        return self._parse_dictionary(serialized)

    def _parse_dictionary(self, dictionary) -> Subtitle:
        subtitle = Subtitle(id=None, quote=None, start_time=None, end_time=None, movie=None)

        if "id" in dictionary:
            subtitle.id = int(dictionary["id"])
        if "quote" in dictionary:
            subtitle.quote = dictionary["quote"]

        return subtitle

    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Subtitle):
                return o.to_dict()
