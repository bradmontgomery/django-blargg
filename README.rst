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
* Write content in HTML

Future Features (maybe)
-----------------------
* Write content in ReSt
* Write content in Markdown

TODO
====
* tests :(
* at least add ReSt support

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

License
=======

This code is distributed under the terms of the MIT license. See the
``LICENSE.txt`` file.


Contributing
============

Feel free to report any issues or (better yet) pull requests for bug fixes!

