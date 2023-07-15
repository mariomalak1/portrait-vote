from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Portrait as Portrait_Model
from .serializers import PortraitSerializer, VotesSerializer, CommentsSerializer
# Create your views here.

@api_view(["GET", "POST"])
def portraits(request):
    if request.method == "GET":
        portrait_objs = Portrait_Model.objects.all()
        serializer = PortraitSerializer(portrait_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        mutible_data = request.data.copy()
        token = mutible_data.get("token")
        if token:
            token = Token.objects.filter(key=token).first()
            if token:
                mutible_data["owner"] = token.user.id
                serializer = PortraitSerializer(data=mutible_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"you must authorize"}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "POST"])
def comments(request):
    pass

@api_view(["GET", "POST"])
def votes(request):
    pass