from apps.movie_quotes.domain.entities.Subtitle import Subtitle

import json


class SubtitleSerializer:
    def serialize(self, subtitle: Subtitle):
        json_subtitle = self.Encoder().encode(subtitle)
        return json_subtitle

    def deserealize(self, json_subtitle) -> Subtitle:
        """
            Subtitles are immutable for client side.
            Thus, for now, just for speed development we will 
            retrive only subtitle id from received json-subtitle string,
            and later get complete subtitle object from repository by 
            this id.
        """
        if type(json_subtitle) is dict:
            id = int(json_subtitle['id'])
        else:                                       # Actual json string
            dictionary = json.loads(json_subtitle)
            id = int(dictionary['id'])

        subtitle = Subtitle(
            id = id
        )

        return subtitle

    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Subtitle):
                return o.to_dict()
