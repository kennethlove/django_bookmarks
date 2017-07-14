from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver

from profiles.models import UserProfile


AUTH_USER_MODEL = get_user_model()

@receiver(post_save, sender=AUTH_USER_MODEL)
def create_profile_handler(sender, instance, **kwargs):
    """As New User created, create and attach Profile"""
    if not kwargs.get('created'):
        return None
    profile = UserProfile(user=instance)
    profile.save()
