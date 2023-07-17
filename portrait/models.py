from django.db import models
from django.contrib.auth.models import User as Django_User_Model
from django.db.models import Count
# Create your models here.

class Comment(models.Model):
    content = models.TextField(null=False)
    owner = models.ForeignKey(Django_User_Model, on_delete=models.CASCADE)
    portrait = models.ForeignKey("Portrait", on_delete=models.CASCADE, related_name="comments")


class Vote(models.Model):
    voter = models.ForeignKey(Django_User_Model, on_delete=models.CASCADE)
    portrait = models.ForeignKey("Portrait", on_delete=models.CASCADE, related_name="votes")


class Portrait(models.Model):
    name = models.CharField(max_length=150, unique=True)
    owner = models.ForeignKey(Django_User_Model, on_delete=models.CASCADE)
    description = models.TextField(null=False)
    photo = models.ImageField(upload_to="Portrait_photos")

    def __str__(self):
        return self.name