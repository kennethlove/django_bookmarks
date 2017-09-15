from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import requests
from django.urls import reverse
from django.utils.text import slugify

from taggit.managers import TaggableManager


class BookmarkManager(models.Manager):
    def get_queryset(self):
        return super(BookmarkManager, self).get_queryset().prefetch_related('tags')

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
    collections = models.ManyToManyField('Collection')
    tags = TaggableManager()
    objects = BookmarkManager()

    def __str__(self):
        return self.title if self.title else self.url

    class Meta:
        unique_together = ('url', 'user')


class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='collections')
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        unique_together = ('user', 'slug')

    def __str__(self):
        return f'{self.user}: {self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:50]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('collections:detail', kwargs={'slug': self.slug})


@receiver(post_save, sender=Bookmark)
def fetch_url_title(sender, instance, created, **kwargs):
    if created:
        r = requests.get(instance.url)
        if r.ok:
            text = r.text
            instance.title = text[text.find('<title>')+7:text.find('</title>')][:255]
            instance.save()
