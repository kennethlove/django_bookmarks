from django.views import generic
from django.shortcuts import get_object_or_404, Http404
from . import models


class ProfileView(generic.DetailView):
    model = models.UserProfile
    template_name = 'profiles/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        obj = get_object_or_404(
            models.UserProfile,
            user=self.request.user
        )
        if obj.user != self.request.user:
            raise Http404
        return obj

class ProfileEditView(generic.UpdateView):
    model = models.UserProfile
    template_name = 'profiles/profile_edit.html'
