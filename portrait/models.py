from django.db import models
# from django.contrib.auth.models import User as Django_User_Model
from django.db.models import Count

from accounts.models import UserProfile
# Create your models here.

class Comment(models.Model):
    content = models.TextField(null=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    portrait = models.ForeignKey("Portrait", on_delete=models.CASCADE, related_name="comments")


class Vote(models.Model):
    voter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    portrait = models.ForeignKey("Portrait", on_delete=models.CASCADE, related_name="votes")


class Portrait(models.Model):
    name = models.CharField(max_length=150, unique=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField(null=False)
    photo = models.URLField(null=False)

    def __str__(self):
        return self.name
