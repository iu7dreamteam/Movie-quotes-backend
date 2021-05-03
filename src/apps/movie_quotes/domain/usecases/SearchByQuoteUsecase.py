from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo

from typing import List

# === Класс, реализующий логику сценария поиска субтитров по цитате ===

class SearchByQuoteUsecase:
    def __init__(self, match_repo, subtitle_repo, quote: str):
        self._match_repo = match_repo
        self._subtitle_repo = subtitle_repo
        self._quote = quote

    # **execute** - воспроизведение сценария
    def execute(self) -> List[Match]:
        subtitles = self._subtitle_repo.find_by_quote_ordered_by_movie(self._quote)
        if len(subtitles) == 0:
            return []

        matches = self._pack_subtitles_into_matches(subtitles)
        for match in matches:
            match.quote = self._quote

        return matches

    # **_pack_subtitles_into_matches** - упаковка найденных субтитров в экземпляры Match для сохранения истории
    def _pack_subtitles_into_matches(self, subtitles) -> List[Match]:
        result_matches = []

        one_movie_subtitles = [subtitles[0]]
        for sub in subtitles:
            if sub == one_movie_subtitles[0]:
                continue

            if sub.movie.id == one_movie_subtitles[-1].movie.id:
                one_movie_subtitles.append(sub)
            else:
                match = Match(
                    movie=one_movie_subtitles[0].movie,
                    subtitles=one_movie_subtitles
                )
                result_matches.append(match)

                one_movie_subtitles = [sub]

        if len(one_movie_subtitles) != 0:
            match = Match(
                movie=one_movie_subtitles[0].movie,
                subtitles=one_movie_subtitles
            )

            result_matches.append(match)

        return result_matches
    