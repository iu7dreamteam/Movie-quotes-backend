from abc import abstractmethod, ABC

from apps.movie_quotes.domain.entities.UserProfile import UserProfile

# === Абстрактный класс для авторизации пользователя ===

class Authorizer(ABC):
    @abstractmethod
    def get_token(self, user_profile: UserProfile) -> str:
        pass
