from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import Signal, receiver
from django.template.defaultfilters import striptags

try:
    blargg_settings = settings.BLARGG
except AttributeError:
    # Use the local settings
    from .settings import BLARGG
    blargg_settings = BLARGG

# -------------------
# Signal Definitions
# -------------------

entry_published = Signal(providing_args=["entry"])


# -------------------
# Signal Handlers
# -------------------

@receiver(entry_published, dispatch_uid='blargg-mail2blogger')
def mail2blogger(entry, **kwargs):
    """This signal handler cross-posts published ``Entry``'s to Blogger.

    """
    enabled = blargg_settings['mail2blogger']
    recipient = blargg_settings['mail2blogger_email']
    if enabled and recipient:

        # Send HTML (and text-only) email
        msg = EmailMultiAlternatives(
            entry.title,  # Subject
            striptags(entry.crossposted_content),  # Text-only
            settings.DEFAULT_FROM_EMAIL,  # From
           [recipient]  # List of Recipients
        )
        msg.attach_alternative(entry.crossposted_content, "text/html")
        msg.send(fail_silently=True)
        # TODO: log this?
