from django.conf.urls import patterns, url
from django.views.generic import ArchiveIndexView, YearArchiveView
from django.views.generic import MonthArchiveView, DayArchiveView
from django.views.generic import ListView

from .models import Entry, Tag

from .views import EntryDetailView
from .views import TaggedEntryListView

# URL examples
# ------------
# /blog/tags/                   -- tag list detail
# /blog/tags/foo/               -- entries tagged with "foo"
# /blog/a-sample-entry/         -- entry detail
# /blog/2013/01/05/             -- entry list (by year, month, day)
# /blog/2013/01/                -- entry list (by year, month)
# /blog/2013/                   -- entry list (by year)
# /blog/2013/05/a-sample-entry/ -- entry detail (with date slug)
# /blog/                        -- entry detail (latest published post)

urlpatterns = patterns('',
    url(r'^tags/$', ListView.as_view(model=Tag), name='list_tags'),
    url(r'^tags/(?P<tag_slug>.*)/$', TaggedEntryListView.as_view(),
        name='tagged_entry_list'),

    # Year, Month, Day Archives
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(
            model=Entry, date_field='published_on', month_format='%m'),
        name='entry_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthArchiveView.as_view(
            model=Entry, date_field='published_on', month_format='%m'),
        name='entry_archive_month'),
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(model=Entry, date_field='published_on'),
        name='entry_archive_year'),

    # Detail views (with and without the date)
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/$',
        EntryDetailView.as_view(), name='entry_detail'),
    url(r'^(?P<slug>.*)/$', EntryDetailView.as_view(), name='entry_detail'),

    url(r'^$',
        ArchiveIndexView.as_view(
            model=Entry, date_field='published_on', paginate_by=10),
        name='list_entries'),
)
