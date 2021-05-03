from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.movie_quotes.domain.usecases.UserRegistrationUseCase import UserRegistrationUseCase, UserAlreadyExists

from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.infrastructure.django.TokenAuthorizer import TokenAuthorizer

# === Класс представления, реализующий post-запросы для регистрации пользователя ===

class RegistrationView(APIView):
    """
    **post** - запрос для передачи данных для регистрации пользователя
    """
    def post(self, request, format=None):
        # **Возвращаемый результат**
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            repeated_password = request.data['repeatedPassword']

            """
            Некорректные формат запроса:
            
            - код 400
            
            - текст ошибки
            
            """

        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        """
        Некорректный повторный ввод пароля:
            
        - код 406
            
        - текст ошибки
            
        """
        if password != repeated_password:
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data='Пароли не совпадают'
            )

        registration_usecase = UserRegistrationUseCase(
            user_profile_repo=UserProfileRepo(),
            authorizer=TokenAuthorizer(),
            username=username,
            password=password,
            email=email
        )

        try:
            result = registration_usecase.execute()

            """
            Успешная регистрация:
            
            - код 200
            
            - логин зарегистрированного пользователя
            
            - почта зарегистрированного пользователя
            
            """

            response = Response(
                status=status.HTTP_200_OK,
                data={
                    'username': result['username'],
                    'email': result['email']
                }
            )
            response.set_cookie(key='token', value=result['token'])

            """
            Совпадение данных с существующим пользователем:
            
            - код 409
            
            - текст ошибки
            
            """

        except UserAlreadyExists:
            response = Response(
                status=status.HTTP_409_CONFLICT,
                data='Пользователь уже существует'
            )

        return response
