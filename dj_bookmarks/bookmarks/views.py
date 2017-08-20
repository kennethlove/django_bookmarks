import operator
from functools import reduce

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import RedirectView

from . import models


class List(LoginRequiredMixin, generic.ListView):
    model = models.Bookmark

    def get_queryset(self):
        queryset = models.Bookmark.objects.current(self.request.user)
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
        return models.Bookmark.objects.current(self.request.user)


class Delete(LoginRequiredMixin, generic.UpdateView):
    fields = ()
    model = models.Bookmark
    success_url = reverse_lazy('bookmarks:list')
    template_name = 'bookmarks/bookmark_confirm_delete.html'

    def get_queryset(self):
        return models.Bookmark.objects.current(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_view'] = True
        return context

    def form_valid(self, form):
        bookmark = form.save(commit=False)
        bookmark.deleted_at = timezone.now()
        bookmark.save()
        return super().form_valid(form)


class Trash(LoginRequiredMixin, generic.ListView):
    model = models.Bookmark

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_view'] = True
        context['trash_view'] = True
        return context

    def get_queryset(self):
        return models.Bookmark.objects.deleted(self.request.user)


class Undelete(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('bookmarks:list')

    def get_object(self):
        return get_object_or_404(
            models.Bookmark,
            user=self.request.user,
            pk=self.kwargs.get('pk'),
            deleted_at__isnull=False
        )

    def get(self, request, *args, **kwargs):
        bookmark = self.get_object()
        bookmark.deleted_at = None
        bookmark.save()
        return super().get(request, *args, **kwargs)


class Search(LoginRequiredMixin, generic.ListView):
    model = models.Bookmark

    def get_queryset(self):
        queryset = models.Bookmark.objects.current(self.request.user)
        q_objects = [
            Q(title__icontains=word) | Q(description__icontains=word)
            for word in self.request.GET.get('q').split()
        ]
        queryset = queryset.filter(reduce(operator.or_, q_objects))
        return queryset
