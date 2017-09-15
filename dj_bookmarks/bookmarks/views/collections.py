from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .. import models


class List(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        return self.request.user.collections.all()


class Detail(LoginRequiredMixin, generic.DetailView):
    def get_queryset(self):
        return self.request.user.collections.all()


class Create(LoginRequiredMixin, generic.CreateView):
    fields = ('name',)
    model = models.Collection

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


