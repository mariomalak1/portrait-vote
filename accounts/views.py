from django.contrib.auth import authenticate, login as django_login, logout as django_logout_user
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from .models import UserProfile
from .serializers import RegisterSerializer, LoginSerializer


# Create your views here.

class CustomAuthentication:
    @staticmethod
    def get_token_or_none(request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if not authorization_header:
            authorization_header = request.data.get("token")
            if not authorization_header:
                return None
        try:
            # Split the header value to extract the token
            auth_type, token = authorization_header.split(' ')
        except:
            token = authorization_header

        if token:
            token_ = Token.objects.filter(key=token).first()
            if token_:
                return token_

        return None


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.create_user()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            token_dict = serializer.create_token(serializer.data, request)
            return Response(token_dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["post"])
def logout(request):
    token_ = CustomAuthentication.get_token_or_none(request)
    if token_ is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    token_.delete()
    try:
        django_logout_user(request)
    except Exception as e:
        print(e)
    return Response(status=status.HTTP_200_OK)
