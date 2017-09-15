from django.conf.urls import url

from ..views import collections as views

urlpatterns = [
    url('^create/$', views.Create.as_view(), name='create'),
    url('^$', views.List.as_view(), name='list'),
]
