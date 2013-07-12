Blargg!
=======

*yet another* Django-powered blog. The goal of this app is to provide a
minimalistic (in both number of features and code) tool for publishing a
mostly-text blog.

This app provides a fairly simple ``Entry`` model, and a light-weight ``Tag``
model.

Features
--------

* Support for ``Site``
* Simple content tagging
* URLs containing an ``Entry``'s publish date (but it still supports other urls
  if you're importing from somewhere else -- trying not to break existing
  content).
* A Management command to import from a really old version of Mezzanine (0.8.5)
* Liberal use of generic views (there's very little custom view code)
* RSS & Atom Feeds
* Sitemap support
* Automatic cross-posting to Blogger (see below)
* Write content in HTML or reStructured Text (requires
  `docutils <https://pypi.python.org/pypi/docutils>`_)

Future Features (maybe)
-----------------------
* Write content in Markdown


Installation
============

This app will probably not be on pypi for the forseeable future. However, you
can install this app with one of the following methods:

1. clone the repo, and put a copy on your python path
2. You can also install the development version with::

    pip install -e git://github.com/bradmontgomery/django-blargg.git#egg=blargg-dev


Once you've got a copy of the code, add ``blargg`` to your ``INSTALLED_APPS``,
and include the following in your Root URLconf::

    url(r'^blog/', include('blargg.urls')),

There are some sample templates under ``blargg/templates/blargg``, but you'll
probably want to override these in your project.


Mail2Blogger Support
====================

This app supports cross-posting to Blogger via email. By default, this setting
is disabled. To enable Mail2Blogger, include the following settings::

    BLARGG = {
        'mail2blogger': True,
        'mail2blogger_email': 'username.SECRET@blogger.com',
    }

To set your Mail2Blogger email address, view your
`Mobile and email <http://www.blogger.com>`_ settings.

Entries that are cross-posted to Blogger will automatically include a link
back to the original site.


License
=======

This code is distributed under the terms of the MIT license. See the
``LICENSE.txt`` file.


Contributing
============

Feel free to report any issues or (better yet) pull requests for bug fixes!


Why "Blargg"
============

From `<http://nintendo.wikia.com/wiki/Blargg>`_:

    A Blargg is a large red dragon that lives in lava and appears in Super Mario
    World. When Mario goes across a lava pit on a pile of skulls occasionally
    the eyes of a Blargg will appear and then itself will try to eat Mario. They
    are found mostly in the Vanilla Dome. Strangely, they have one lazy eye.

Other than that, *Blargg* is really fun to say out loud. Especially if you use
a *Pirate Voice*. Go ahead, try it!

*Blargg*.
