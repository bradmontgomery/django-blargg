#!/usr/bin/env python
# -*- coding: utf-8 -*-
from string import ascii_letters
from random import choice

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings
from django.urls import reverse

from ..models import Tag, Entry


@override_settings(SITE_ID=1)
@override_settings(ROOT_URLCONF='blargg.tests.urls')
class TestViews(TestCase):

    def setUp(self):
        username = ''.join([choice(ascii_letters) for i in range(10)])
        User = get_user_model()
        user = User.objects.create(
            username=username,
            password='{0}@example.com'.format(username)
        )

        # Sample Entry
        self.entry = Entry(
            site=Site.objects.get(pk=settings.SITE_ID),
            author=user,
            title="Test Entry",
            raw_content="Test Content",
            tag_string="foo, bar"
        )
        self.entry.publish()  # Calls .save()

        # Sample Tag (should have foo, bar tags from entry's tag_string)
        self.tag = Tag.objects.get(name="foo")

    def test_list_tags(self):
        url = reverse('blargg:list_tags')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 2)

    def test_tagged_entry_list(self):
        url = reverse('blargg:tagged_entry_list', args=[self.tag.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 1)

    def test_entry_archive_day(self):
        # NOTE: Entries are stored in UTC and the EntryDayArchiveView converts
        # dates to the local timezone (if USE_TZ=True).
        # Also, Entry.get_absolute_url also converts to TIME_ZONE if USE_TZ is
        # True.
        y, m, d = self.entry.published_on.strftime("%Y-%m-%d").split("-")
        url = reverse('blargg:entry_archive_day', args=[y, m, d])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertTemplateUsed("blargg/entry_archive_day.html")

    def test_entry_archive_month(self):
        y, m, d = self.entry.published_on.strftime("%Y-%m-%d").split("-")
        url = reverse('blargg:entry_archive_month', args=[y, m])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertIn('date_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 1)
        self.assertEqual(len(resp.context['date_list']), 1)
        self.assertTemplateUsed("blargg/entry_archive_month.html")

    def test_entry_archive_year(self):
        y, m, d = self.entry.published_on.strftime("%Y-%m-%d").split("-")
        url = reverse('blargg:entry_archive_year', args=[y])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('date_list', resp.context)
        self.assertEqual(len(resp.context['date_list']), 1)
        self.assertTemplateUsed("blargg/entry_archive_year.html")

    def test_entry_detail_with_date(self):
        y, m, d = self.entry.published_on.strftime("%Y-%m-%d").split("-")
        url = reverse('blargg:entry_detail', args=[y, m, d, self.entry.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object', resp.context)
        self.assertIsInstance(resp.context['object'], Entry)
        self.assertTemplateUsed("blargg/entry_detail.html")

    def test_entry_detail_without_date(self):
        url = reverse('blargg:entry_detail', args=[self.entry.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object', resp.context)
        self.assertIsInstance(resp.context['object'], Entry)
        self.assertTemplateUsed("blargg/entry_detail.html")

    def test_list_entries(self):
        """Tests the ARchiveIndexView."""
        url = reverse('blargg:list_entries')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 1)
        self.assertTemplateUsed("blargg/entry_list.html")
