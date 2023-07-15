import os
from django.db import models
from django.contrib.auth.models import User
from project import settings
# Create your models here.

class UserProfile(models.Model):
    def upload_to(instance, filename):
        file_extension = filename.split(".")[-1]
        filename = instance.user.username + "." + file_extension
        # Media/Users_Profile_Photo/marioportrait_o86CwMa.jpg
        # Media/Users_Profile_Photo/mario@portrait.jpg
        path = os.path.join("Users_Profile_Photo", filename)
        full_path = os.path.join(settings.MEDIA_ROOT, path)

        print(full_path)
        print(os.path.exists(full_path))
        if os.path.exists(full_path):
            print("HEHE")
            # File with the same name exists, delete it
            os.remove(full_path)

        return path


    photo = models.ImageField(upload_to=upload_to, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

