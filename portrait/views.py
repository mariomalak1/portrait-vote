from django.shortcuts import render
from .serializers import PortraitSerializer, VotesSerializer, CommentsSerializer
# Create your views here.


def rr(request):
    print(VotesSerializer().__repr__())
    print("@"*50)
    print(PortraitSerializer().__repr__())
    print("@"*50)
    print(CommentsSerializer().__repr__())
    print("@"*50)
