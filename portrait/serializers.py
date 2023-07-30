from rest_framework import serializers

from .models import Portrait as Portrait_Model, Comment, Vote
from accounts.serializers import UserSerializer
from accounts.models import UserProfile

class CommentsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self, instance):
        user_serializer = UserSerializer(instance.owner)
        return user_serializer.data

    class Meta:
        model = Comment
        fields = '__all__'

class NormalCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PortraitSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    votes = serializers.SerializerMethodField(read_only=True)
    owner = serializers.SerializerMethodField(read_only=True)
    voted = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Portrait_Model
        fields = "__all__"

    def get_voted(self, instance):
        if self.context:
            user_request = self.context["user_request"]
            if user_request:
                for vote in instance.votes.all():
                    if vote.voter == user_request:
                        return 1
        return 0


    def get_owner(self, instance):
        owner_serializer = UserSerializer(instance.owner)
        return owner_serializer.data

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

class PortraitsVotedByUser(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["portrait"]