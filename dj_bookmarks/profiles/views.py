from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, Http404

from . import forms
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
    form_class = forms.ProfileForm
    model = models.UserProfile
    template_name = 'profiles/profile_edit.html'
    success_url = reverse_lazy('accounts:view')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        self.request.user.first_name = form.cleaned_data['first_name']
        self.request.user.last_name = form.cleaned_data['last_name']
        self.request.user.save()
        return super().form_valid(form)
