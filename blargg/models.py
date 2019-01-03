import pytz
import re

from collections import Counter
try:
    from docutils.core import publish_parts as docutils_publish
    assert docutils_publish  # placate flake8
except ImportError:  # pragma: no cover
    docutils_publish = None  # pragma: no cover

try:
    from markdown import markdown
    assert markdown  # placate flake8
except ImportError:  # pragma: no cover
    markdown = None  # pragma: no cover

from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.timezone import now as utc_now
from django.utils.timezone import make_naive

from .signals import entry_published


class TagManager(models.Manager):
    def create_tags(self, entry):
        """Inspects an ``Entry`` instance, and builds associates ``Tag``
        objects based on the values in the ``Entry``'s ``tag_string``."""
        tag_list = [t.lower().strip() for t in entry.tag_string.split(',')]
        for t in tag_list:
            tag, created = self.get_or_create(name=t)
            entry.tags.add(tag)


class Tag(models.Model):
    """A *really* light-weight tagging class."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, editable=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def save(self, *args, **kwargs):
        """Generate a unique slug for each tag."""
        self.name = self.name.lower().strip()
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blargg:tagged_entry_list', args=[self.slug])

    objects = TagManager()


class Entry(models.Model):
    CONTENT_FORMAT_CHOICES = (
        ('md', 'Markdown'),
        ('rst', 'reStructured Text'),
        ('html', 'HTML'),
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=256)

    raw_content = models.TextField(help_text="Content entered by the author.")
    content_format = models.CharField(
        max_length=4,
        choices=CONTENT_FORMAT_CHOICES
    )
    rendered_content = models.TextField(editable=False)
    published = models.BooleanField(
        default=False,
        blank=True,
        help_text="Show this entry to the public"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="A slug/url used to identify this entry."
    )
    date_slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
        help_text="A slug/url used to identify this entry; also includes "
                  "the date on which the entry was published."
    )

    tag_string = models.TextField(
        blank=True,
        help_text="A comma-separated list of tags."
    )
    tags = models.ManyToManyField(Tag, editable=False)

    published_on = models.DateTimeField(blank=True, null=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_on', 'title']
        get_latest_by = 'published_on'
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    def _create_slug(self):
        """Generates a slug from the Title."""
        # Don't overwrite any existing slugs by default.
        if not self.slug:
            self.slug = slugify(self.title)

    def _create_date_slug(self):
        """Prefixes the slug with the ``published_on`` date."""
        if not self.pk:
            # haven't saved this yet, so use today's date
            d = utc_now()
        elif self.published and self.published_on:
            # use the actual published on date
            d = self.published_on
        elif self.updated_on:
            # default to the last-updated date
            d = self.updated_on
        self.date_slug = u"{0}/{1}".format(d.strftime("%Y/%m/%d"), self.slug)

    def _render_content(self):
        """Renders the content according to the ``content_format``."""
        if self.content_format == "rst" and docutils_publish is not None:
            doc_parts = docutils_publish(
                source=self.raw_content,
                writer_name="html4css1"
            )
            self.rendered_content = doc_parts['fragment']
        elif self.content_format == "rs" and docutils_publish is None:
            raise RuntimeError("Install docutils to pubilsh reStructuredText")
        elif self.content_format == "md" and markdown is not None:
            self.rendered_content = markdown(self.raw_content)
        elif self.content_format == "md" and markdown is None:
            raise RuntimeError("Install Markdown to pubilsh markdown")
        else:  # Assume we've got html
            self.rendered_content = self.raw_content

    def _set_published(self):
        """Set the fields that need to be set in order for this thing to
        appear "Published", and send the ``entry_published`` signal."""
        self.published = True
        self.published_on = utc_now()
        return True

    def save(self, *args, **kwargs):
        """Auto-generate a slug from the name."""
        self._create_slug()
        self._create_date_slug()
        self._render_content()

        # Call ``_set_published`` the *first* time this Entry is published.
        # NOTE: if this is unpublished, and then republished, this method won't
        # get called; e.g. the date won't get changed and the
        # ``entry_published`` signal won't get re-sent.
        send_published_signal = False
        if self.published and self.published_on is None:
            send_published_signal = self._set_published()

        super(Entry, self).save(*args, **kwargs)

        # We need an ID before we can send this signal.
        if send_published_signal:
            entry_published.send(sender=self, entry=self)

    def get_absolute_url(self):
        """URL based on the entry's slug."""
        return reverse('blargg:entry_detail', args=[self.slug])

    def get_absolute_url_with_date(self):
        """URL based on the entry's date & slug."""
        pub_date = self.published_on

        if pub_date and settings.USE_TZ:
            # If TZ is enabled, convert all of these dates from UTC to whatever
            # the project's timezone is set as. Ideally, we'd pull this form
            # some user settings, but the *canonical* publish time is that of
            # the author (asssuming author == owner of this project).
            pub_date = make_naive(pub_date, pytz.utc)  # Make naive
            pub_date = pytz.timezone(settings.TIME_ZONE).localize(pub_date)
        if pub_date:
            args = [
                pub_date.strftime("%Y"),
                pub_date.strftime("%m"),
                pub_date.strftime("%d"),
                self.slug
            ]
        else:
            args = [self.slug]
        return reverse('blargg:entry_detail', args=args)

    def publish(self):
        """Puplish & Save."""
        self._set_published()
        self.save()

    def unpublish(self):
        self.published = False
        self.published_on = None
        self.save()

    @property
    def tag_list(self):
        """Return a plain python list containing all of this Entry's tags."""
        tags = [tag.strip() for tag in self.tag_string.split(",")]
        return sorted(filter(None, tags))

    @property
    def content(self):
        safe_content = mark_safe(self.rendered_content)
        return safe_content

    @property
    def crossposted_content(self):
        """Content to be cross-posted on other sites. This method adds an
        additional line of content with a link back to the original site as
        well as the `#end` tag. This signals the end blog content according
        to: https://support.google.com/blogger/answer/41452?hl=en

        """
        url = "http://{0}{1}".format(self.site.domain, self.get_absolute_url())
        origin = (
            '<p><em>This entry was originally published at: '
            '<a href="{0}">{1}</a>.</em></p>#end'.format(url, url)
        )
        return mark_safe(u"{0}{1}".format(self.content, origin))


@receiver(post_save, sender=Entry, dispatch_uid='generate-entry-tags')
def generate_entry_tags(sender, instance, created, raw, using, **kwargs):
    """Generate the M2M ``Tag``s for an ``Entry`` right after it has
    been saved."""
    Tag.objects.create_tags(instance)


# Words we want to ignore when calculating entry stats, below.
IGNORE_WORDS = "a,an,and,the,but,to,it,its,is,on,of,if,in,with,for,at,this,that,so"
IGNORE_WORDS = IGNORE_WORDS.split(',')


def entry_stats(entries, top_n=10):
    """Calculates stats for the given ``QuerySet`` of ``Entry``s."""

    wc = Counter()  # A Word counter
    for content in entries.values_list("rendered_content", flat=True):
        # Do a little cleanup
        content = strip_tags(content)  # remove all html tags
        content = re.sub('\s+', ' ', content)  # condense all whitespace
        content = re.sub('[^A-Za-z ]+', '', content)  # remove non-alpha chars

        words = [w.lower() for w in content.split()]
        wc.update([w for w in words if w not in IGNORE_WORDS])

    return {
        "total_words": len(wc.values()),
        "most_common": wc.most_common(top_n),
    }
