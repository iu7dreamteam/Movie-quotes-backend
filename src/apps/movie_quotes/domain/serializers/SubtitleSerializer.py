from apps.movie_quotes.domain.entities.Subtitle import Subtitle

import json

# === Класс представления для конвертации из/в формат словаря (json) экземпляра Subtitle ===

class SubtitleSerializer:
    # **serialize** - конвертация в json
    def serialize(self, subtitle: Subtitle):
        json_subtitle = self.Encoder().encode(subtitle)
        return json_subtitle

    # **deserialize** - конвертация из json в экземпляр Subtitle
    def deserealize(self, serialized) -> Subtitle:
        if isinstance(serialized, str):
            serialized = json.loads(serialized)
        return self._parse_dictionary(serialized)

    # **_parse_dictionary** - парсер словаря и запись полей словаря в экземпляр Subtitle
    def _parse_dictionary(self, dictionary) -> Subtitle:
        subtitle = Subtitle(id=None, quote=None, start_time=None, end_time=None, movie=None)

        if "id" in dictionary:
            subtitle.id = int(dictionary["id"])
        if "quote" in dictionary:
            subtitle.quote = dictionary["quote"]

        return subtitle

    # === Вспомогательный класс конвертации, наследующий методы json.JSONEncoder ===

    class Encoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Subtitle):
                return o.to_dict()
