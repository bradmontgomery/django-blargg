from django.conf.urls import patterns, url
from .views import EntryDetailView, EntryListView
from .views import TagListView, TaggedEntryListView

# URL examples
# ------------
# /blog/tags/                   -- tag list detail
# /blog/tags/foo/               -- entries tagged with "foo"
# /blog/a-sample-entry/         -- entry detail
# /blog/2013/                   -- entry list (by year)
# /blog/2013/01/                -- entry list (by year, month)
# /blog/2013/05/                -- entry list (by year, month, day)
# /blog/2013/05/a-sample-entry/ -- entry detail (with date slug)
# /blog/                        -- entry detail (latest published post)
# /blog/preview/id/             -- entry detail for unpublished Entry

urlpatterns = patterns('',
    url(r'^tags/$', TagListView.as_view(), name='list_tags'),
    url(r'^tags/(?P<tag_slug>.*)/$', TaggedEntryListView.as_view(),
        name='tagged_entry_list'),

    #url(r'^/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$$', '', name=''),
    url(r'^(?P<slug>.*)/$', EntryDetailView.as_view(), name='entry_detail'),
    url(r'^$', EntryListView.as_view(), name='list_entries'),
)
