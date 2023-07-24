import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from project import settings
# Create your models here.

class UserProfile(AbstractUser):
    image = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.username

