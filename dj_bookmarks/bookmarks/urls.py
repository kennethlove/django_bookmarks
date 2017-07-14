from django.conf.urls import url

from . import views

urlpatterns = [
    url('^create/$', views.Create.as_view(), name='create'),
    url('^update/(?P<pk>\d+)/$', views.Update.as_view(), name='update'),
    url('^delete/(?P<pk>\d+)/$', views.Delete.as_view(), name='delete'),
    url('^$', views.List.as_view(), name='list'),
]