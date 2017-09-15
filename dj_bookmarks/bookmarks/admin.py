from django.contrib import admin

from . import models

@admin.register(models.Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'user']
    filter_horizontal = ['collections',]


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

