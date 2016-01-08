from django.conf.urls import url, include
from django.contrib.sitemaps import views as sitemaps_views
from blargg.sitemaps import EntrySitemap


sitemaps = {
    'blog': EntrySitemap,
}


urlpatterns = [
    url(r'^blog/', include('blargg.urls', namespace='blargg')),

    # Sitemaps
    url(
        r'^sitemap\.xml$',
        sitemaps_views.index,
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}
    ),
    url(
        r'^sitemap-(?P<section>.+)\.xml$',
        sitemaps_views.sitemap,
        {'sitemaps': sitemaps},
        name='sitemaps'
    ),
]
