History
-------


## 0.7.0 (2019-01-03)

- Django 2 support (2.1.4)
- Added `on_delete` options for FK fields.
- Added title/description settings for feeds.
- Converted `url` use to `path` function in urlconf.
- Removed old south migrations.
- Include words to ignore when generating word stats.
- Add `Entry.tag_list` method that returns a sorted list of tag names


## 0.6.0 (2016-12-13)

- Django 1.8/1.9 support (with django migrations)
- Python 3 support
- Removing old, proably worthless management command
- Support for pluggable User models.
- Support for Markdown
- Adding to pypi


## 0.5.2 (2016-01-04)

- fixes for tests
- correctly count words on EntryYearArchive View

## 0.5.1 (2016-01-03)

- includes tags in the TaggedEntryListView

## 0.5.0 (2015-05-03)

- Removed dates from URLs
- Admin improvements


## 0.4.3 and earlier (2014-07-16)

- haphazardly built this thing
