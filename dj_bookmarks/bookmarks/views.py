from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from . import models


class List(LoginRequiredMixin, generic.ListView):
    model = models.Bookmark

    def get_queryset(self):
        queryset = self.request.user.bookmarks.filter(deleted_at__isnull=True)
        tag = self.kwargs.get('tag')
        if tag:
            queryset = queryset.filter(tags__name__in=[tag])
        return queryset


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


class Delete(LoginRequiredMixin, generic.UpdateView):
    fields = ()
    model = models.Bookmark
    success_url = reverse_lazy('bookmarks:list')
    template_name = 'bookmarks/bookmark_confirm_delete.html'

    def get_queryset(self):
        return self.request.user.bookmarks.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_view'] = True
        return context

    def form_valid(self, form):
        bookmark = form.save(commit=False)
        bookmark.deleted_at = timezone.now()
        bookmark.save()
        return super().form_valid(form)
