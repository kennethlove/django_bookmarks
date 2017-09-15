from django.conf.urls import url

from ..views import collections as views

urlpatterns = [
    url('^create/$', views.Create.as_view(), name='create'),
    url('^c:(?P<slug>[-\w]+)/$', views.Detail.as_view(), name='detail'),
    url('^$', views.List.as_view(), name='list'),
]
