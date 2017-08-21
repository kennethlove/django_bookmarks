from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from taggit.managers import TaggableManager

from . import functions


class BookmarkManager(models.Manager):
    def deleted(self, user):
        return user.bookmarks.filter(deleted_at__isnull=False)

    def current(self, user):
        return user.bookmarks.filter(deleted_at__isnull=True)


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bookmarks')
    url = models.URLField('URL')
    title = models.CharField(default='', blank=True, max_length=255)
    description = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager()
    objects = BookmarkManager()

    def __str__(self):
        return self.title if self.title else self.url

    class Meta:
        unique_together = ('url', 'user')


@receiver(post_save, sender=Bookmark)
def fetch_bookmark_url_title(sender, instance, created, **kwargs):
    if created and not instance.title:
        title = functions.fetch_url_title(instance.url)
        if title:
            instance.title = title[:255]
            instance.save()
