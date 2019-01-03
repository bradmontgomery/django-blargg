from django import template
from django.urls import reverse
from blargg.models import Entry

register = template.Library()


@register.simple_tag
def entry_archive_year_url():
    """Renders the ``entry_archive_year`` URL for the latest ``Entry``."""
    entry = Entry.objects.filter(published=True).latest()
    arg_list = [entry.published_on.strftime("%Y")]
    return reverse('blargg:entry_archive_year', args=arg_list)
