from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import Signal, receiver
from django.template.defaultfilters import striptags

try:
    blargg_settings = settings.BLARGG
except AttributeError:  # pragma: no cover
    # Use the local settings
    from .settings import BLARGG  # pragma: no cover
    blargg_settings = BLARGG  # pragma: no cover

# -------------------
# Signal Definitions
# -------------------

entry_published = Signal(providing_args=["entry"])


# -------------------
# Signal Handlers
# -------------------

@receiver(entry_published, dispatch_uid='blargg-mail2blogger')
def mail2blogger(entry, **kwargs):
    """This signal handler cross-posts published ``Entry``'s to Blogger. For
    this to work, the following settings must be non-False; e.g.:

        BLARGG = {
            'mail2blogger': True,
            'mail2blogger_email': 'user@example.com',
        }

    """
    enabled = blargg_settings.get('mail2blogger', False)
    recipient = blargg_settings.get('mail2blogger_email', None)
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
