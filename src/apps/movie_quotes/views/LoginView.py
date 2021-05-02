from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.infrastructure.django.TokenAuthorizer import TokenAuthorizer

from apps.movie_quotes.domain.usecases.UserLoginUseCase import UserLoginUseCase, IncorrectPassword


class LoginView(APIView):
    def post(self, request, format=None):
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        login_usecase = UserLoginUseCase(
            user_profile_repo=UserProfileRepo(),
            authorizer=TokenAuthorizer(),
            email=email,
            password=password
        )

        try:
            result = login_usecase.execute()

            response = Response(
                status=status.HTTP_200_OK,
                data={
                    'username': result['username'],
                    'email': result['email']
                }
            )
            response.set_cookie(key='token', value=result['token'])

        except IncorrectPassword:
            response = Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data='Не существует пользователя с такой почтой или паролем'
            )

        return response
