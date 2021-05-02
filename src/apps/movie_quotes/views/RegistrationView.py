from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.movie_quotes.domain.usecases.UserRegistrationUseCase import UserRegistrationUseCase, UserAlreadyExists

from apps.movie_quotes.domain.repositories.UserProfileRepo import UserProfileRepo
from apps.movie_quotes.infrastructure.django.TokenAuthorizer import TokenAuthorizer


class RegistrationView(APIView):
    def post(self, request, format=None):
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            repeated_password = request.data['repeatedPassword']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if password != repeated_password:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        registration_usecase = UserRegistrationUseCase(
            user_profile_repo=UserProfileRepo(),
            authorizer=TokenAuthorizer(),
            username=username,
            password=password,
            email=email
        )

        try:
            result = registration_usecase.execute()
            response = Response(
                status=status.HTTP_200_OK,
                data={
                    'username': result['username'],
                    'email': result['email']
                }
            )
            response.set_cookie(key='token', value=result['token'])
        except UserAlreadyExists:
            response = Response(status=status.HTTP_409_CONFLICT)

        return response
