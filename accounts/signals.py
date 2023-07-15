from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, created, instance, *args, **kwargs):
    if created:
        profile_ = UserProfile.objects.create(user=instance)
        profile_.save()
        return profile_
