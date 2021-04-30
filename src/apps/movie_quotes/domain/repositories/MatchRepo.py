from apps.movie_quotes.domain.entities.Match import Match
from apps.movie_quotes.domain.entities.UserProfile import UserProfile
from apps.movie_quotes.domain.entities.Movie import Movie

from apps.movie_quotes.domain.repositories.MovieRepo import MovieRepo
from apps.movie_quotes.domain.repositories.SubtitleRepo import SubtitleRepo
from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo

from apps.movie_quotes.infrastructure.django.models.MatchORM import MatchORM

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from typing import List


class MatchRepo:
    def save(self, match: Match) -> Match:
        """
        Saves given match object if it exists in database,
        othervise creates a new
        """
        if match.id is None:
            saved_match = self._create(match)
        else:
            if MatchORM.objects.filter(pk=match.id).exists():
                match.movie = MovieRepo().save(match.movie)

                subtitle_repo = SubtitleRepo()
                for sub in match.subtitles:
                    sub = subtitle_repo.save(sub)
            else:
                saved_match = self._create(match)

        return saved_match

    def get(self, id) -> Match:
        return self.Mapper.to_domain(MatchORM.objects.get(pk=id))

    def filter_by_user(self, user_profile: UserProfile) -> List[Match]:
        user_profile_orm = UserProfileRepo().Mapper.from_domain(user_profile)
        query = MatchORM.objects.filter(user_profile=user_profile_orm)
        query = query.order_by('-id')

        result_query = []
        for match in query:
            result_query.append(self.Mapper.to_domain(match))

        return result_query

    def filter_by_movie_and_user(self, movie: Movie, user_profile: UserProfile) -> List[Match]:
        movie_orm = MovieRepo().Mapper.from_domain(movie)
        user_profile_orm = UserProfileRepo().Mapper.from_domain(user_profile)

        query = MatchORM.objects.filter(movie=movie_orm,
                                        user_profile=user_profile_orm)
        result_query = []
        for match in query:
            result_query.append(self.Mapper.to_domain(match))

        return result_query


    #def create_or_update(self, match: Match) -> Match:
    #    if match.id is not None:
    #        try:
    #            MatchORM.objects.get(pk=match.id)
    #            match = self._update(match)
    #        except ObjectDoesNotExist:
    #            match = self.create(match)
    #
    #    return match
    #
    #def _update(self, match: Match) -> Match:
    #    match_orm = MatchORM.objects.get(pk=match.id)
    #
    #    subtitle_repo = SubtitleRepo()
    #    subtitles_orm = []
    #    for sub_domain in match.subtitles:
    #        subtitles_orm.append(subtitle_repo.Mapper.from_domain(sub_domain))
    #
    #    match_orm.subtitles.set(subtitles_orm)
    #    match_orm.save()
    #
    #    return self.Mapper.to_domain(match_orm)
    #
    #def create(self, match: Match) -> Match:
    #    subtitle_repo = SubtitleRepo()
    #    subtitles_orm = []
    #    for sub_domain in match.subtitles:
    #        subtitles_orm.append(subtitle_repo.Mapper.from_domain(sub_domain))
    #
    #    user_profile_orm = UserProfileRepo().Mapper.from_domain(match.user_profile)
    #
    #    match_orm = MatchORM.objects.create(
    #        user_profile=user_profile_orm,
    #        movie=MovieRepo().Mapper.from_domain(match.movie)
    #    )
    #
    #    match_orm.subtitles.set(subtitles_orm)
    #    match_orm.save()
    #
    #    return self.Mapper.to_domain(match_orm)
    #

    def _create(self, match: Match) -> Match:
        if match.user_profile is None:
            raise NoUserDefinedForMatch()

        movie = MovieRepo().save(match.movie)
        movie_orm = MovieRepo.Mapper.from_domain(movie)

        subtitle_repo = SubtitleRepo()
        subtitles = [subtitle_repo.save(sub) for sub in match.subtitles]
        subtitles_orm = [SubtitleRepo.Mapper.from_domain(sub) for sub in subtitles]

        user_profile_orm = UserProfileRepo.Mapper.from_domain(match.user_profile)

        created_match = MatchORM.objects.create(
            user_profile=user_profile_orm,
            movie=movie_orm
        )

        created_match.subtitles.set(subtitles_orm)
        created_match.save()

        return self.Mapper.to_domain(created_match)


    class Mapper:
        @staticmethod
        def to_domain(match_orm: MatchORM) -> Match:
            movie_domain = MovieRepo.Mapper.to_domain(match_orm.movie)

            subtitles_domain = []
            for sub in match_orm.subtitles.all().order_by('-id'):
                subtitles_domain.append(SubtitleRepo.Mapper.to_domain(sub))

            user_profile = UserProfileRepo().get(match_orm.user_profile.id)

            match_domain = Match(
                id=match_orm.id,
                user_profile=user_profile,
                movie=movie_domain,
                subtitles=subtitles_domain
            )

            return match_domain

        @staticmethod
        def from_domain(match: Match) -> MatchORM:
            """
            Match is immutable object. It should't be changed in domain logic at all.
            Thus we can provide mapping from domain object to ORM object just by
            returning it's existing ORM instance by primary key.
            """
            return MatchORM.objects.get(pk=match.id)


class NoUserDefinedForMatch(Exception):
    def __init__(self, message=''):
        super().__init__("Can't save match in the database \
                          without user_profile link" + message)
