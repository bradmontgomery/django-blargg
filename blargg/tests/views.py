#!/usr/bin/env python
# -*- coding: utf-8 -*-
from string import ascii_letters
from random import choice

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Tag, Entry


class TestViews(TestCase):

    def setUp(self):
        username = ''.join([choice(ascii_letters) for i in range(10)])
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
        url = reverse('list_tags')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 2)

    def test_tagged_entry_list(self):
        url = reverse('tagged_entry_list', args=[self.tag.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 1)

    # wat
    #def test_entry_archive_day(self):
        #y, m, d = self.entry.published_on.strftime("%Y-%m-%d").split("-")
        #url = reverse('entry_archive_day', args=[y, m, d])
        #resp = self.client.get(url)
        #self.assertEqual(resp.status_code, 200)
        #self.assertIn('object_list', resp.context)
        #self.assertEqual(len(resp.context['object_list']), 1)
        #self.assertTemplateUsed("blargg/entry_archive_day.html")

    def test_entry_archive_month(self):
        y, m, d = self.entry.published_on.strftime("%Y-%m-%d").split("-")
        url = reverse('entry_archive_month', args=[y, m])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertIn('date_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 1)
        self.assertEqual(len(resp.context['date_list']), 1)
        self.assertTemplateUsed("blargg/entry_archive_month.html")

    def test_entry_archive_year(self):
        y, m, d = self.entry.published_on.strftime("%Y-%m-%d").split("-")
        url = reverse('entry_archive_year', args=[y])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('date_list', resp.context)
        self.assertEqual(len(resp.context['date_list']), 1)
        self.assertTemplateUsed("blargg/entry_archive_year.html")

    def test_entry_detail_with_date(self):
        y, m, d = self.entry.published_on.strftime("%Y-%m-%d").split("-")
        url = reverse('entry_detail', args=[y, m, d, self.entry.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object', resp.context)
        self.assertIsInstance(resp.context['object'], Entry)
        self.assertTemplateUsed("blargg/entry_detail.html")

    def test_entry_detail_without_date(self):
        url = reverse('entry_detail', args=[self.entry.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object', resp.context)
        self.assertIsInstance(resp.context['object'], Entry)
        self.assertTemplateUsed("blargg/entry_detail.html")

    def test_list_entries(self):
        """Tests the ARchiveIndexView."""
        url = reverse('list_entries')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertEqual(len(resp.context['object_list']), 1)
        self.assertTemplateUsed("blargg/entry_list.html")
