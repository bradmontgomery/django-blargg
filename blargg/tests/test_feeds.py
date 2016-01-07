from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings

from ..feeds import RSSEntriesFeed, AtomEntriesFeed
from ..models import Entry


@override_settings(SITE_ID=1)
class TestRSSEntriesFeed(TestCase):

    def setUp(self):
        # Some setup (need a User and an Entry)
        User = get_user_model()
        username = 'blargg'
        user = User.objects.create(
            username=username,
            password='{0}@example.com'.format(username)
        )
        self.entry = Entry(
            site=Site.objects.get(pk=settings.SITE_ID),
            author=user,
            title="Test Entry",
            raw_content="Test Content",
            content_format="html"
        )
        self.entry.publish()  # calls .save()

        self.unpublished_entry = Entry(
            site=Site.objects.get(pk=settings.SITE_ID),
            author=user,
            title="Test Entry",
            raw_content="Test Content",
            content_format="html",
            published=False
        )
        self.entry.save()

        self.feed = RSSEntriesFeed()

    def test_items(self):
        """Verify that ``.items()`` returns a queryset of published Entries"""
        published_entries = list(Entry.objects.filter(published=True))
        feed_entries = list(self.feed.items())
        self.assertEqual(feed_entries, published_entries)
        self.assertNotIn(self.unpublished_entry, feed_entries)

    def test_item_title(self):
        self.assertEqual(self.feed.item_title(self.entry), self.entry.title)

    def test_item_description(self):
        self.assertEqual(
            self.feed.item_description(self.entry),
            self.entry.content
        )


@override_settings(SITE_ID=1)
class TestAtomEntriesFeed(TestCase):
    """NOTE: This whole test is a duplicate of ``TestRSSEntriesFeed``."""
    def setUp(self):
        # Some setup (need a User and an Entry)
        User = get_user_model()
        username = 'blargg'
        user = User.objects.create(
            username=username,
            password='{0}@example.com'.format(username)
        )
        self.entry = Entry(
            site=Site.objects.get(pk=settings.SITE_ID),
            author=user,
            title="Test Entry",
            raw_content="Test Content",
            content_format="html"
        )
        self.entry.publish()  # calls .save()

        self.unpublished_entry = Entry(
            site=Site.objects.get(pk=settings.SITE_ID),
            author=user,
            title="Test Entry",
            raw_content="Test Content",
            content_format="html",
            published=False
        )
        self.entry.save()

        self.feed = AtomEntriesFeed()

    def test_items(self):
        """Verify that ``.items()`` returns a queryset of published Entries"""
        published_entries = list(Entry.objects.filter(published=True))
        feed_entries = list(self.feed.items())
        self.assertEqual(feed_entries, published_entries)
        self.assertNotIn(self.unpublished_entry, feed_entries)

    def test_item_title(self):
        self.assertEqual(self.feed.item_title(self.entry), self.entry.title)

    def test_item_description(self):
        self.assertEqual(
            self.feed.item_description(self.entry),
            self.entry.content
        )
