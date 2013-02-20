"""
This module contains classes for both RSS and Atom feeds. To use these, you'll
need to set up a couple of URL patterns; e.g.

    from blargg.feeds import RSSEntriesFeed, AtomEntriesFeed

    urlpatterns = patterns('',
        (r'^feed/rss/$', RSSEntriesFeed()),
        (r'^feed/atom/$', AtomEntriesFeed()),
    )

"""

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Entry


class RSSEntriesFeed(Feed):
    """An RSS feed for all ``Entry``'s"""
    title = "brad's blog"
    link = "/blog/"
    description = "Entries from brad's blog"

    def items(self):
        return Entry.objects.filter(published=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.rendered_content


class AtomEntriesFeed(RSSEntriesFeed):
    feed_type = Atom1Feed
    subtitle = RSSEntriesFeed.description
