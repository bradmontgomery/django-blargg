from django.conf.urls import url, include
from blargg.sitemaps import EntrySitemap


sitemaps = {
    'blog': EntrySitemap,
}


# Sitemaps
urlpatterns = [
    url(r'^blog/', include('blargg.urls', namespace='blargg')),
    url(
        r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.index',
        {'sitemaps': sitemaps}
    ),
    url(
        r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}
    ),
]
