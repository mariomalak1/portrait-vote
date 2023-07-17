from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view, APIView, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Portrait as Portrait_Model, Comment, Vote
from .serializers import PortraitSerializer, CommentsSerializer, VoteSerializer
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
    # function to get portrait obj and return it to post and get, patch
    @staticmethod
    def get_portrait_or_error(request):
        portrait_id_ = request.data.get("portrait_id")
        try:
            portrait_obj = get_object_or_404(Portrait_Model, id=portrait_id_)
            return portrait_obj
        except Exception as e:
            return e

    def post(self, request):
        token_ = CustomAuthentication.get_token_or_none(request)
        print(token_)
        if not token_:
            return Response({"error": "you must authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # get the portrait obj
        portrait_obj = self.get_portrait_or_error(request)
        if not isinstance(portrait_obj, Portrait_Model):
            return Response({"error": str(portrait_obj)}, status=status.HTTP_404_NOT_FOUND)

        mutible_data = request.data.copy()
        mutible_data["owner"] = token_.user.id
        mutible_data["portrait"] = portrait_obj.id
        serializer = CommentsSerializer(data=mutible_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "you must authorize"}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        portrait_obj = self.get_portrait_or_error(request)
        if not isinstance(portrait_obj, Portrait_Model):
            return Response({"error": str(portrait_obj)}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(portrait_id=portrait_obj.id).all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VoteView(APIView):
    def post(self, request):
        token_ = CustomAuthentication.get_token_or_none(request)
        if not token_:
            return Response({"error": "you must authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        portriat_obj = CommnetView.get_portrait_or_error(request)

        if not isinstance(portriat_obj, Portrait_Model):
            return Response({"error": str(portriat_obj)}, status=status.HTTP_404_NOT_FOUND)

        vote_on_portrait = Vote.objects.filter(portrait_id=portriat_obj.id).filter(voter_id=token_.user.id).first()

        if vote_on_portrait:
            vote_on_portrait.delete()
            return Response({"message":f"Voted removed from {portriat_obj.name}"})
        else:
            Vote.objects.create(portrait=portriat_obj, voter=token_.user)
            return Response({"message":f"Voted Done On {portriat_obj.name}"})

    # get all votes on specific portrait
    def get(self, request):
        token_ = CustomAuthentication.get_token_or_none(request)
        if not token_:
            return Response({"error": "you must authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        portriat_obj = CommnetView.get_portrait_or_error(request)

        if not isinstance(portriat_obj, Portrait_Model):
            return Response({"error": str(portriat_obj)}, status=status.HTTP_404_NOT_FOUND)

        votes = Vote.objects.filter(portrait_id=portriat_obj.id).all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PortraitDetails(APIView):
    def get(self, request):
        # get the portrait obj
        portrait_obj = CommnetView.get_portrait_or_error(request)
        if not isinstance(portrait_obj, Portrait_Model):
            return Response({"error": str(portrait_obj)}, status=status.HTTP_404_NOT_FOUND)
        serializer = PortraitSerializer(portrait_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        token_ = CustomAuthentication.get_token_or_none(request)
        if not token_:
            return Response({"error": "you must authorized"}, status=status.HTTP_401_UNAUTHORIZED)

        portrait_obj = CommnetView.get_portrait_or_error(request)
        if not isinstance(portrait_obj, Portrait_Model):
            return Response({"error": str(portrait_obj)}, status=status.HTTP_404_NOT_FOUND)

        if portrait_obj.owner.id != token_.user.id:
            return Response({"error":"You not Permetied to do that"}, status=status.HTTP_403_FORBIDDEN)

        serializer = PortraitSerializer(data=request.data, instance=portrait_obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
