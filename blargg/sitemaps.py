"""
This module defines a default Sitemap for ``Entry``'s. To enable sitemaps,
you'll need to configure your project's URL patters with something like:

    from blargg.sitemaps import EntrySitemap

    sitemaps = {'blog': EntrySitemap}

    urlpatterns = patterns('',

        url(
            r'^sitemap\.xml$',
            'django.contrib.sitemaps.views.sitemap',
            {'sitemaps': sitemaps}
        )
    )

"""
from django.contrib.sitemaps import Sitemap
from .models import Entry


class EntrySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Entry.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_on
