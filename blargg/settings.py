"""
Custom settings for django-blargg.

* ``mail2blogger`` -- enable Mail2Blogger. Published entries will be
  cross-posted to Blogger.
* ``mail2blogger_email`` -- the email address to which published entries are
  mailed.

"""

BLARGG = {
    'title': 'A Blargg Blog',
    'description': 'Blog Entries',
    'mail2blogger': False,
    'mail2blogger_email': '',
}
