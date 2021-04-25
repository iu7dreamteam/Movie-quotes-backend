from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo

from typing import List


class ShowUserHistoryUsecase:
    def __init__(self, user_profile: UserProfile, user_profile_repo, match_repo):
        self._user_profile = user_profile
        self._user_profile_repo = user_profile_repo
        self._match_repo = match_repo

    def execute(self) -> List[Match]:
        user_matches = self._match_repo.filter_by_user(self._user_profile)
        return user_matches
