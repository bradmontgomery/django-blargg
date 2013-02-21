from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import Signal, receiver

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
        send_mail(
            entry.title,  # Subject
            entry.crossposted_content,  # Content
            settings.DEFAULT_FROM_EMAIL,  # From
           [recipient],  # List of Recipients
           fail_silently=False
        )
        # TODO: log this?
