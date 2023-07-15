from rest_framework import serializers
from .models import Portrait as Portrait_Model, Comment, Vote

class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PortraitSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()
    class Meta:
        model = Portrait_Model
        fields = "__all__"

    def get_comments(self, instance):
        all_comments = Comment.objects.filter(portrait_id=instance.id)
        # commnets_serializer = CommentsSerializer(all_comments)
        return all_comments
        return commnets_serializer.data

    def get_votes(self, instance):
        vote_number = Vote.objects.filter(portrait_id=instance.id).count()
        return vote_number



