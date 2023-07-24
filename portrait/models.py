from django.db import models

from accounts.models import UserProfile
# Create your models here.

class Comment(models.Model):
    content = models.TextField(null=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    portrait = models.ForeignKey("Portrait", on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    voter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    portrait = models.ForeignKey("Portrait", on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)


class Portrait(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField(null=False)
    photo = models.URLField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
