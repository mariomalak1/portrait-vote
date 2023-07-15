from rest_framework import serializers
from .models import Portrait as Portrait_Model, Comment, Vote

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PortraitSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    votes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Portrait_Model
        fields = "__all__"

    def get_comments(self, instance):
        all_comments = Comment.objects.filter(portrait_id=instance.id).all()
        serializer_comment = CommentsSerializer(all_comments, many=True)
        return serializer_comment.data

    def get_votes(self, instance):
        vote_number = Vote.objects.filter(portrait_id=instance.id).count()
        return vote_number



