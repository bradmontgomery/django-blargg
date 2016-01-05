from django.views.generic import DetailView, ListView
from django.views.generic import DayArchiveView, MonthArchiveView
from django.views.generic import YearArchiveView
from django.views.generic.list import MultipleObjectMixin

from .models import Entry, entry_stats


class EntryStatsMixin(MultipleObjectMixin):
    """This mixin will calculate entry stats (counting words) for a View's
    queryset of objects."""

    def get_context_data(self, **kwargs):
        context = super(EntryStatsMixin, self).get_context_data(**kwargs)

        # Calculate stats for the queryset of Entries & add to the context.
        objects = context['object_list']
        if not objects.exists() and 'date_list' in context and context['date_list']:
            # EntryYearArchiveViews won't include any objects, so query for
            # thos using the year
            years = list(set(dt.year for dt in context['date_list']))
            if len(years) > 0:
                objects = Entry.objects.filter(published_on__year=years[0])

        context.update(entry_stats(objects))
        return context


class TaggedEntryListView(ListView):
    """List all ``Entry``s that have the given ``Tag``(s). Mulitple ``Tag``s
    may be separated by a plus; For example: /blog/tags/foo+bar would retrieve
    all ``Entry``s tagged with both "foo" and "bar".

    """
    allow_empty = True
    model = Entry
    tags = None

    def get_queryset(self):
        tag_list = self.kwargs['tag_slug'].split('+')
        self.tags = filter(lambda x: len(x) > 0, tag_list)
        return Entry.objects.filter(tags__slug__in=self.tags).distinct()

    def get_context_data(self, **kwargs):
        context = super(TaggedEntryListView, self).get_context_data(**kwargs)
        context['tags'] = self.tags
        return context


class EntryDetailView(DetailView):
    """Detail for an ``Entry``."""
    model = Entry
    slug_field = 'slug'


# Year, Month, Day Archives
# -------------------------

class EntryYearArchiveView(EntryStatsMixin, YearArchiveView):
    queryset = Entry.objects.filter(published=True)
    date_field = "published_on"
    year_format = '%Y'
    template_name = "blargg/entry_archive_year.html"


class EntryMonthArchiveView(EntryStatsMixin, MonthArchiveView):
    queryset = Entry.objects.filter(published=True)
    date_field = "published_on"
    year_format = '%Y'
    month_format = "%m"
    template_name = "blargg/entry_archive_month.html"


class EntryDayArchiveView(EntryStatsMixin, DayArchiveView):
    # NOTE: Entries are stored in UTC and this view converts dates to the
    # local timezone (if USE_TZ=True). Therefore, Entry.get_absolute_url also
    # converts to TIME_ZONE if USE_TZ=True.
    queryset = Entry.objects.filter(published=True)
    date_field = "published_on"
    year_format = '%Y'
    month_format = "%m"
    day_format = "%d"
    template_name = "blargg/entry_archive_day.html"
    allow_empty = True
