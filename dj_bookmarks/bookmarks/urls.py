from django.conf.urls import url

from . import views

urlpatterns = [
    url('^create/$', views.Create.as_view(), name='create'),
    url('^trash/$', views.Trash.as_view(), name='trash'),
    url('^search/$', views.Search.as_view(), name='search'),
    url('^update/(?P<pk>\d+)/$', views.Update.as_view(), name='update'),
    url('^delete/(?P<pk>\d+)/$', views.Delete.as_view(), name='delete'),
    url('^undelete/(?P<pk>\d+)/$', views.Undelete.as_view(), name='undelete'),
    url('^t:(?P<tag>[-\w]+)/$', views.List.as_view(), name='tag_search'),
    url('^$', views.List.as_view(), name='list'),
]