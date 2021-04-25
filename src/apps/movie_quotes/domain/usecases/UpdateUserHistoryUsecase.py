from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.repositories.MatchRepo import MatchRepo
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo

from typing import List


class UpdateUserHistoryUsecase:
    def __init__(self, user_profile: UserProfile, match_to_save: Match, match_repo):
        self._user_profile = user_profile
        self._match_to_save = match_to_save
        self._match_repo = match_repo

    def execute(self):
        self._match_to_save = self._match_repo.create(self._match_to_save)
