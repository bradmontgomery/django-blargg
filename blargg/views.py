from django.views.generic import DetailView, ListView

from .models import Entry, Tag


class TagListView(ListView):
    """List all ``Tag`` instances."""
    model = Tag


class TaggedEntryListView(ListView):
    """List all ``Entry``s that have a given ``Tag``."""
    allow_empty = True
    model = Entry

    def get_queryset(self):
        tag_list = self.kwargs['tag_slug'].split('+')
        tags = filter(lambda x: len(x) > 0, tag_list)
        return Entry.objects.filter(tags__slug__in=tags).distinct()


class EntryDetailView(DetailView):
    """Detail for an ``Entry``."""
    model = Entry
    slug_field = 'slug'

class EntryListView(ListView):
    """List all ``Entry``s."""
    model = Entry


