from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/edit/$', views.ProfileEditView.as_view(), name='edit_profile'),
]
