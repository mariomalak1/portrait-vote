from rest_framework import serializers
from .models import Portrait as Portrait_Model, Comment, Vote

from accounts.serializers import UserSerializer

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PortraitSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    votes = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Portrait_Model
        fields = "__all__"

    def get_owner(self, instance):
        return instance.owner.username

    def get_comments(self, instance):
        all_comments = Comment.objects.filter(portrait_id=instance.id).all()
        serializer_comment = CommentsSerializer(all_comments, many=True)
        return serializer_comment.data

    def get_votes(self, instance):
        vote_number = Vote.objects.filter(portrait_id=instance.id).count()
        return vote_number

    def create_protrait(self, data_):
        self.validated_data["owner"] = data_.get("owner")
        return self.save()

    def is_valid(self, raise_exception=False):
        if self.partial:
            for field in self.fields.values():
                field.required = False
        return super().is_valid(raise_exception=raise_exception)


class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.SerializerMethodField()
    class Meta:
        model = Vote
        fields = ["voter"]

    def get_voter(self, instance):
        return UserSerializer(instance.voter).data



