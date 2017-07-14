from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from . import models


class List(LoginRequiredMixin, generic.ListView):
    model = models.Bookmark

    def get_queryset(self):
        return self.request.user.bookmarks.all()


class Create(LoginRequiredMixin, generic.CreateView):
    fields = ('url', 'title', 'description', 'tags')
    model = models.Bookmark
    success_url = reverse_lazy('bookmarks:list')

    def form_valid(self, form):
        bookmark = form.save(commit=False)
        bookmark.user = self.request.user
        bookmark.save()
        form.save_m2m()
        return super().form_valid(form)


class Update(LoginRequiredMixin, generic.UpdateView):
    fields = ('url', 'title', 'description', 'tags')
    model = models.Bookmark
    success_url = reverse_lazy('bookmarks:list')

    def get_queryset(self):
        return self.request.user.bookmarks.all()


class Delete(LoginRequiredMixin, generic.DeleteView):
    model = models.Bookmark
    success_url = reverse_lazy('bookmarks:list')

    def get_queryset(self):
        return self.request.user.bookmarks.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_view'] = True
        return context
