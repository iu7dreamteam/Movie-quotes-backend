from typing import List

from apps.movie_quotes.domain.entities.Subtitle import Subtitle

from pysubparser import parser
from pysubparser.cleaners import formatting
import chardet


class SubtitleParser:

    @staticmethod
    def parse(filename: str) -> List[Subtitle]:
        encoding = SubtitleParser._detect_encoding(filename)

        raw_subtitles = parser.parse(filename, encoding=encoding)
        raw_subtitles = formatting.clean(raw_subtitles)

        subtitle_entities = []

        for raw_subtitle in raw_subtitles:
            subtitle_entity = Subtitle(
                quote=raw_subtitle.text,
                start_time=raw_subtitle.start,
                end_time=raw_subtitle.end
            )
            
            subtitle_entities.append(subtitle_entity)

        return subtitle_entities


    @staticmethod
    def _detect_encoding(filename: str) -> str:
        with open(filename, 'rb') as file:
            data = file.read()
            meta = chardet.detect(data)
            return meta['encoding']
