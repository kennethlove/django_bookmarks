from django.conf.urls import url

from . import views

urlpatterns = [
    url('^create/$', views.Create.as_view(), name='create'),
    url('^update/(?P<pk>\d+)/$', views.Update.as_view(), name='update'),
    url('^$', views.List.as_view(), name='list'),
]