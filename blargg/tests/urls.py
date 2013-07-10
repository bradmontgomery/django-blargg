from django.conf.urls import patterns, url
from blargg.sitemaps import EntrySitemap

sitemaps = {
    'blog': EntrySitemap,
}


# Sitemaps
urlpatterns = patterns('django.contrib.sitemaps.views',
    url(r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        'sitemap',
        {'sitemaps': sitemaps}
    ),
)
