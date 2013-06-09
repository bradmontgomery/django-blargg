from django.http import Http404
from django.views.generic import DetailView, ListView
from django.views.generic import DayArchiveView, MonthArchiveView
from django.views.generic import YearArchiveView

from .models import Entry


class TaggedEntryListView(ListView):
    """List all ``Entry``s that have the given ``Tag``(s). Mulitple ``Tag``s
    may be separated by a plus; For example: /blog/tags/foo+bar would retrieve
    all ``Entry``s tagged with both "foo" and "bar".

    """
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

    def get_object(self, **kwargs):
        """Make sure the ``Entry`` contains the correct date if it was
        specified."""
        obj = super(EntryDetailView, self).get_object(**kwargs)

        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)

        if year and month and day:
            # IF the dates are different, throw a fit!
            try:
                assert obj.published_on.year == int(year)
                assert obj.published_on.month == int(month)
                assert obj.published_on.day == int(day)
            except AssertionError:
                raise Http404

        return obj


# Year, Month, Day Archives
# -------------------------

class EntryYearArchiveView(YearArchiveView):
    model = Entry
    date_field = "published_on"


class EntryMonthArchiveView(MonthArchiveView):
    model = Entry
    date_field = "published_on"
    month_format = "%m"


class EntryDayArchiveView(DayArchiveView):
    model = Entry
    date_field = "published_on"
    month_format = "%m"
