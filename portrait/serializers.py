from rest_framework import serializers
from .models import Portrait as Portrait_Model, Comment, Vote

class PortraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portrait_Model
        fields = "__all__"

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'