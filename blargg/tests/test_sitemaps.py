#!/usr/bin/env python
# -*- coding: utf-8 -*-
from string import ascii_letters
from random import choice

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase

from ..models import Entry


class TestEntrySitemap(TestCase):
    url = 'blargg.tests.urls'

    def setUp(self):
        username = ''.join([choice(ascii_letters) for i in range(10)])
        User = get_user_model()
        user = User.objects.create(
            username=username,
            password='{0}@example.com'.format(username)
        )
        self.entry = Entry(
            site=Site.objects.get(pk=settings.SITE_ID),
            author=user,
            title="Test Entry",
            raw_content="Test Content",
            tag_string="foo, bar, baz",
        )
        self.entry.publish()  # Calls save

    def test_sitemap_root(self):
        # The root sitemap doc should include a link to the blog
        resp = self.client.get('/sitemap.xml')
        self.assertEqual(resp.status_code, 200)
        self.assertIn("sitemap-blog.xml", resp.content)

    def test_sitemap_blog(self):
        # The sitemap for blogs should contain a link to an Entry
        resp = self.client.get('/sitemap-blog.xml')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.entry.get_absolute_url(), resp.content)
