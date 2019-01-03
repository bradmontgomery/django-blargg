"""
This module contains classes for both RSS and Atom feeds. To use these, you'll
need to set up a couple of URL patterns; e.g.

    from blargg.feeds import RSSEntriesFeed, AtomEntriesFeed

    urlpatterns = patterns('',
        (r'^feed/rss/$', RSSEntriesFeed()),
        (r'^feed/atom/$', AtomEntriesFeed()),
    )

"""
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Entry
from .settings import BLARGG


def _get_setting(name):
    try:
        return settings.BLARGG[name]
    except (AttributeError, KeyError):
        return BLARGG[name]


class RSSEntriesFeed(Feed):
    """An RSS feed for all ``Entry``'s"""
    title = _get_setting("title")
    link = "/blog/"
    description = _get_setting("description")

    def items(self):
        return Entry.objects.filter(published=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.rendered_content


class AtomEntriesFeed(RSSEntriesFeed):
    feed_type = Atom1Feed
    subtitle = RSSEntriesFeed.description
