"""
This command will import content from a JSON dump of mezzanine 0.8.5
(which is *really* old) blogposts.

"""
from datetime import datetime
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import get_current_timezone

from blargg.models import Entry

class Command(BaseCommand):
    args = '<path-to-json-export>'
    help = """Import blogposts from a mezzanine 0.8.5 JSON dump."""

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("\nYour Arguments are Invalid!\n\n")

        # associate each import post with the default Site
        try:
            site = Site.objects.get(pk=settings.SITE_ID)
        except Site.DoesNotExist:
            msg = "\nMake sure you've set a SITE_ID setting.\n"
            raise CommandError(msg)

        f = open(args[0], 'r')
        imported_posts = json.loads(f.read())
        f.close()

        # fields from mezzanine.blog.blogpost (assuming version 0.8.5)
        # ------------------------------------------------------------
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

        for post in imported_posts:
            # Only import the ``blogpost`` objects; ignore the comments for now
            if post['model'] == "blog.blogpost":
                data = post['fields']

                # Just assume all the users are the same... this may be a
                # horribly inaccurate assumption :-/
                try:
                    # Use the default user if there's no user data in the
                    # JSON file
                    u = User.objects.get(id=data.get('user', 1))
                except User.DoesNotExist:
                    msg = "\nFailed to find the Author for the Post.\n"
                    raise CommandError(msg)

                entry = Entry()
                entry.site = site
                entry.author = u
                entry.title = data['title']
                entry.raw_content = data['content']
                entry.content_format = 'html'
                entry.rendered_content = data['content']
                entry.slug = data['slug']

                # Filter out any zero-length tags
                tag_list = filter(lambda s: len(s) > 0,
                                  data['_keywords'].split())
                entry.tag_string = ', '.join(tag_list)
                entry.save()

                # If an ``Entry`` is marked "published" prior to saving, it'll
                # use "today" as the publish date. We have to save once, then
                # "publish" it with an older date.
                if data['publish_date']:
                    fmt = "%Y-%m-%d %H:%M:%S"  # Date format String
                    date_str = data['publish_date']  # Grab the date string
                    tz = get_current_timezone()  # assumen current timezone
                    d = datetime.strptime(date_str, fmt).replace(tzinfo=tz)
                    entry.published_on = d
                    entry.published = True

                entry.save()


                output = "- Added: {0}\n".format(entry)
                self.stdout.write(output)
        self.stdout.write("\nDone!\n\n")
