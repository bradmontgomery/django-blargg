from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings

from ..models import Entry
from ..admin import TagAdmin, EntryAdmin


@override_settings(SITE_ID=1)
class TestTagAdmin(TestCase):
    """Verify expected fields on ``TagAdmin`` class"""
    def test_list_display(self):
        self.assertEqual(TagAdmin.list_display, ('name', 'slug'))

    def test_search_fields(self):
        self.assertEqual(TagAdmin.search_fields, ('name', ))


@override_settings(SITE_ID=1)
class TestEntryAdmin(TestCase):
    """Verify fields and methods on ``EntryAdmin`` class."""

    def test_list_display(self):
        expected = sorted([
            'title',
            'content_format',
            'author',
            'published',
            'published_on',
            'updated_on'
        ])
        self.assertEqual(sorted(EntryAdmin.list_display), expected)

    def test_date_hierarchy(self):
        self.assertEqual(EntryAdmin.date_hierarchy, 'created_on')

    def test_list_filter(self):
        self.assertEqual(EntryAdmin.list_filter, ('published', 'content_format'))

    def test_search_fields(self):
        expected = ('title', 'raw_content', 'tag_string')
        self.assertEqual(EntryAdmin.search_fields, expected)

    def test_prepopulated_fields(self):
        self.assertEqual(EntryAdmin.prepopulated_fields, {"slug": ("title", )})

    def test_actions(self):
        self.assertEqual(EntryAdmin.actions, ['publish_entries'])

    def test_publish_entries(self):
        # Some setup (need a User and an Entry)
        User = get_user_model()
        username = 'entryadmin_publish_entries'
        user = User.objects.create(
            username=username,
            password='{0}@example.com'.format(username)
        )
        entry = Entry(
            site=Site.objects.get(pk=settings.SITE_ID),
            author=user,
            title="Test Entry",
            raw_content="Test Content",
        )
        entry.save()
        self.assertFalse(entry.published)

        # Create an EntryAdmin and call the `publish_entries` method
        admin = EntryAdmin(Entry, AdminSite())
        admin.publish_entries(None, Entry.objects.all())

        # Fetch the Entry, and see if it's published.
        entry = Entry.objects.get(pk=entry.id)
        self.assertTrue(entry.published)
