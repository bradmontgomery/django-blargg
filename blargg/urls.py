from django.urls import path
from django.views.generic import ArchiveIndexView
from django.views.generic import ListView

from .models import Entry, Tag
from .views import (
    EntryDayArchiveView,
    EntryDetailView,
    EntryMonthArchiveView,
    EntryYearArchiveView,
    TaggedEntryListView,
)

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

app_name = 'blargg'
urlpatterns = [
    path('tags/', ListView.as_view(model=Tag), name='list_tags'),
    path(
        'tags/<slug:tag_slug>/',
        TaggedEntryListView.as_view(),
        name='tagged_entry_list'
    ),

    # Year, Month, Day Archives
    path(
        '<int:year>/<int:month>/<int:day>/',
        EntryDayArchiveView.as_view(),
        name='entry_archive_day'
    ),
    path(
        '<int:year>/<int:month>/',
        EntryMonthArchiveView.as_view(),
        name='entry_archive_month'
    ),
    path(
        '<int:year>/',
        EntryYearArchiveView.as_view(),
        name='entry_archive_year'
    ),

    # Detail views (with and without the date)
    path(
        '<int:year>/<int:month>/<int:day>/<slug:slug>/',
        EntryDetailView.as_view(),
        name='entry_detail'
    ),
    path('<slug:slug>/', EntryDetailView.as_view(), name='entry_detail'),
    path(
        '',
        ArchiveIndexView.as_view(
            model=Entry,
            date_field='published_on',
            paginate_by=10
        ),
        name='list_entries'
    ),
]
