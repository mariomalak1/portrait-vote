from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view, APIView, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Portrait as Portrait_Model, Comment
from .serializers import PortraitSerializer, CommentsSerializer

# Create your views here.

class CustomAuthentication:
    @staticmethod
    def get_token_or_none(request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if authorization_header:
            # Split the header value to extract the token
            auth_type, token = authorization_header.split(' ')
            token_ = Token.objects.filter(key=token).first()
            if token_:
                return token_

        return None


class Portratis(APIView):
    def get(self, request):
        portrait_objs = Portrait_Model.objects.annotate(vote_count=Count('votes')).order_by('-vote_count')
        serializer = PortraitSerializer(portrait_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        token_ = CustomAuthentication.get_token_or_none(request)
        if not token_:
            return Response({"error": "you must authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        mutible_data = request.data.copy()
        mutible_data["owner"] = token_.user
        serializer = PortraitSerializer(data=mutible_data)
        if serializer.is_valid():
            serializer.create_protrait(mutible_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommnetView(APIView):
    # function to get portrait id and return it to post and get, patch
    def get_portrait_id(self, request):
        portrait_id_ = request.data.get("portrait_id")
        try:
            get_object_or_404(Portrait_Model, id=portrait_id_)
            return int(portrait_id_)
        except Exception as e:
            return e

    def post(self, request):
        token_ = CustomAuthentication.get_token_or_none(request)
        if not token_:
            return Response({"error": "you must authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # get the portrait id
        portrait_id_ = self.get_portrait_id(request)
        if not isinstance(portrait_id_, int):
            return Response({"error": str(portrait_id_)}, status=status.HTTP_404_NOT_FOUND)

        mutible_data = request.data.copy()
        mutible_data["owner"] = token_.user.id
        mutible_data["portrait"] = portrait_id_
        serializer = CommentsSerializer(data=mutible_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "you must authorize"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        portrait_id_ = self.get_portrait_id(request)
        if not isinstance(portrait_id_, int):
            return Response({"error": str(portrait_id_)}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(portrait_id=portrait_id_).all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PortraitDetails(APIView):
    def get(self, request):
        portrait_id = request.data.get("portrait_id")
        portrait_obj = get_object_or_404(Portrait_Model, id=portrait_id)
        serializer = PortraitSerializer(portrait_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        portrait_id = request.data.get("portrait_id")
        portrait_obj = get_object_or_404(Portrait_Model, id=portrait_id)
        serializer = PortraitSerializer(data=request.data, instance=portrait_obj, partial=True)

        if serializer.is_valid():
            pass


