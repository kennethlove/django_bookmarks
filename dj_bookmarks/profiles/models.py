from django.contrib.auth import get_user_model
from django.db import models

AUTH_USER_MODEL = get_user_model()

def avatar_upload_path(instance, filename):
    """
    Builds the media path for where it will store
    the avatar images.
    """
    return os.path.join('avatars', 'user_{0}', '{1}').format(
        instance.user.id, filename)


class UserProfile(models.Model):
    """A Basic User Profile"""
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        primary_key=True,
        related_name='profile'
    )
    avatar = models.ImageField(
        'Avatar picture',
        upload_to=avatar_upload_path,
        null=True,
        blank=True
    )
    bio = models.TextField("Short Bio", default='')

    @property
    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        return '{}'.format(self.user.get_username())

    @property
    def get_avatar_url(self):
        if self.avatar:
            return '/media/{}'.format(self.avatar)
        return '/media/default.jpg'

    def __str__(self):
        return "{}'s profile".format(self.user.get_username())
