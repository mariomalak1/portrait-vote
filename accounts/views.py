from django.contrib.auth import authenticate, login as django_login
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, LoginSerializer
# Create your views here.

class RegisterView(APIView):
	def post(self, request):
		data = request.data
		serializer = RegisterSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
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