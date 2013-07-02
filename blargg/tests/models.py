#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from ..models import TagManager, Tag, Entry


class TestTagManager(TestCase):

    def setUp(self):
        self.tagmanager = TagManager()


class TestTag(TestCase):
    urls = "blargg.urls"

    def setUp(self):
        self.tag = Tag(name="Test Tag")
        self.tag.save()

    def test__unicode__(self):
        self.assertEqual(self.tag.__unicode__(), u"test tag")

    def test_save(self):
        """Verify that tag names get lowercased & stripped, while slugs are
        slugified."""
        t = Tag(name="   Foo Tag   ")
        self.assertEqual(t.slug, '')
        t.save()
        self.assertEqual(t.name, u"foo tag")
        self.assertEqual(t.slug, u"foo-tag")

    def test_get_absolute_url(self):
        self.assertIn("tags/test-tag/", self.tag.get_absolute_url())


class TestEntry(TestCase):

    def setUp(self):
        self.entry = Entry()
