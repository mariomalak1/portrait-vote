import os
from django.db import models
from django.contrib.auth.models import User
from project import settings
# Create your models here.

class UserProfile(User):
    def upload_to(instance, filename):
        file_extension = filename.split(".")[-1]
        filename = instance.username + "." + file_extension
        path = os.path.join("Users_Profile_Photo", filename)
        full_path = os.path.join(settings.MEDIA_ROOT, path)

        if os.path.exists(full_path):
            # File with the same name exists, delete it
            os.remove(full_path)
        return path

    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    def __str__(self):
        return self.username

