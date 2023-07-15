from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login

from .models import UserProfile


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["image"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=250)
    last_name = serializers.CharField(max_length=100, required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    # photo = serializers.SerializerMethodField()
    photo = serializers.FileField(allow_empty_file=False, allow_null=False, use_url=True)


    def validate_username(self, username):
        user = User.objects.filter(username=username).first()
        if user:
            raise serializers.ValidationError("this username is already taken")
        return username

    def create(self, validated_data):
        print("validated_data :", validated_data)
        new_user = User.objects.create(username=validated_data.get("username"))
        new_user.set_password(validated_data.get("password"))
        if validated_data.get("last_name"):
            new_user.last_name = validated_data.get("last_name")
        if validated_data.get("first_name"):
            new_user.first_name = validated_data.get("first_name")
        new_user.save()

        photo_file = validated_data.get("photo")
        if photo_file:
            profile_ = UserProfile.objects.filter(user=new_user).first()
            profile_.photo = photo_file
            profile_.save()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

    def validate(self, data):
        user = User.objects.filter(username=data.get("username")).first()
        if not user:
            raise serializers.ValidationError("Username Not Found")
        return data

    def create_token(self, data, request):
        user = authenticate(username=data.get("username"), password=data.get("password"))
        django_login(request, user=user)
        token = Token.objects.filter(user=user).first()
        if not token:
            token = Token.objects.create(user=user)
        return {"token": str(token)}
