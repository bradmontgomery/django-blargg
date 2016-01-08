Blargg!
=======

*yet another* Django-powered blog. The goal of this app is to provide a
minimalistic (in both number of features and code) tool for publishing a
mostly-text blog. Shameless plug: see
`bradmontgomery.net <https://bradmontgomery.net>`_ for an example.

This app provides a fairly simple ``Entry`` model, and a light-weight ``Tag``
model.

Features
--------

* Support for ``Site``
* Simple content tagging
* RSS & Atom Feeds
* Sitemap support
* Automatic cross-posting to Blogger (see below)
* Support authoring content in reStructured Text (requires
  `docutils <https://pypi.python.org/pypi/docutils>`_), markdown (requires
  `Markdown <https://pypi.python.org/pypi/Markdown>`_) or plain old HTML.

Installation
------------

1. Install with `pip install django-blargg`
2. Add ``blargg`` to your ``INSTALLED_APPS``
3. Configure your Root URLconf: ``url(r'^blog/', include('blargg.urls', namespace='blargg'))``
4. Customize your templates. There are some sample templates under
   ``blargg/templates/blargg``, but you'll want to override these in your project.
5. (Optinally) enable Mail2Blogger (see below)


Mail2Blogger Support
--------------------

This app supports cross-posting to Blogger via email. By default, this setting
is disabled. To enable Mail2Blogger, include the following settings::

    BLARGG = {
        'mail2blogger': True,
        'mail2blogger_email': 'username.SECRET@blogger.com',
    }

To set your Mail2Blogger email address, view your
`Mobile and email <http://www.blogger.com>`_ settings. Entries that are
cross-posted to Blogger will automatically include a link back to the original
site (provided that you've got the ``django.contrib.sites`` app installed and
configured correctly).

**Warning**: *mail2blogger* appears to remove extra whitespace from your content
which breaks things in a ``<pre>`` or ``<code>`` blocks. If you know how to
prevent this,
`please let me know <https://github.com/bradmontgomery/django-blargg/issues/3>`_.

License
-------

This code is distributed under the terms of the MIT license. See the
``LICENSE.txt`` file.


Contributing
------------

Feel free to report any issues or (better yet) pull requests for bug fixes!
There's a `requirements.txt` file in this repo to help you get all the
dependencies you'll likely need (for python3).


Why the name "Blargg"?
----------------------

From `<http://nintendo.wikia.com/wiki/Blargg>`_:

    A Blargg is a large red dragon that lives in lava and appears in Super Mario
    World. When Mario goes across a lava pit on a pile of skulls occasionally
    the eyes of a Blargg will appear and then itself will try to eat Mario. They
    are found mostly in the Vanilla Dome. Strangely, they have one lazy eye.

Other than that, *Blargg* is really fun to say out loud. Especially if you use
a *Pirate Voice*. Go ahead, try it!

*Blargg*.

