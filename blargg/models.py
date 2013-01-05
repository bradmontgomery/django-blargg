from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
#from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe


class TagManager(models.Manager):
    def create_tags(self, entry):
        """Inspects an ``Entry`` instance, and builds associates ``Tag``
        objects based on the values in the ``Entry``'s ``tag_string``."""
        tag_list = [t.lower().strip() for t in entry.tag_string.split(',')]
        for t in tag_list:
            try:
                # only add the tag if it's not aleady associated with the entry
                tag_obj, created = self.get_or_create(name=t)
                if tag_obj.name not in entry.tags.values_list('name', flat=True):
                    entry.tags.add(tag_obj)
            except IntegrityError:
                pass  # just ignore any tags that are duplicates


class Tag(models.Model):
    """A *really* light-weight tagging class."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, editable=False, unique=True)

    def __unicode__(self):
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
        #return reverse()
        return '/tags'

    objects = TagManager()


class Entry(models.Model):
    CONTENT_FORMAT_CHOICES = (
        ('html', 'HTML'),
        ('md', 'Markdown'),
        ('rst', 'reStructured Text'),
    )

    site = models.ForeignKey(Site)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=256)

    raw_content = models.TextField(help_text="Content entered by the author.")
    content_format = models.CharField(max_length=4,
        choices=CONTENT_FORMAT_CHOICES)
    rendered_content = models.TextField(editable=False)

    published = models.BooleanField(default=False, blank=True,
        help_text="Show this entry to the public")
    slug = models.SlugField(max_length=255, unique=True,
        help_text="A slug/url used to identify this entry.")
    date_slug = models.SlugField(max_length=255, unique=True, editable=False,
        help_text="A slug/url used to identify this entry; also includes "
                  "the date on which the entry was published.")

    tag_string = models.TextField(blank=True,
        help_text="A comma-separated list of tags.")
    tags = models.ManyToManyField(Tag, editable=False)

    published_on = models.DateTimeField(blank=True, null=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    # fields from mezzanine.blog.blogpost
    # -----------------------------------
    # - id
    # - status (2 == published)
    # - category (always null)
    # - description
    # - title
    # - short_url (seems to always be null)
    # - content
    # - expiry_date
    # - publish_date
    # - user
    # - slug
    # - keywords [list of integers]
    # - _keywords (a string with space-separated keywords)
    # -

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-published_on', 'title']
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
            d = datetime.today()
        elif self.published and self.published_on:
            # use the actual published on date
            d = self.published_on
        elif self.updated_on:
            # default to the last-updated date
            d = self.updated_on
        self.date_slug = u"{0}/{1}".format(d.strftime("%Y-%m-%d"), self.slug)

    def _render_content(self):
        """Renders the content according to the ``content_format``."""
        if self.content_format == "html":
            self.rendered_content = self.raw_content
        elif self.content_format == "md":
            raise NotImplementedError  # TODO: run thru markdown!
            self.rendered_content = self.raw_content
        elif self.content_fromat == "rst":
            raise NotImplementedError  # TODO: run thru markdown!
            self.rendered_content = self.raw_content

    def save(self, *args, **kwargs):
        """Auto-generate a slug from the name."""
        self._create_slug()
        self._create_date_slug()
        self._render_content()
        super(Entry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        #return reverse('', args=[self.slug])
        return '/'

    def publish(self):
        self.published = True
        self.published_on = datetime.now()
        self.save()

    def unpublish(self):
        self.published = False
        self.published_on = None
        self.save()

    @property
    def content(self):
        safe_content = mark_safe(self.rendered_content)
        return safe_content

@receiver(post_save, sender=Entry, dispatch_uid='generate-entry-tags')
def generate_entry_tags(sender, instance, created, raw, using, **kwargs):
    """Generate the M2M ``Tag``s for an ``Entry`` right after it has
    been saved."""
    Tag.objects.create_tags(instance)
