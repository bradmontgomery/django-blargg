from django.contrib import admin
from . import models


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )


class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'content_format', 'author', 'published',
        'published_on', 'updated_on'
    )
    date_hierarchy = 'created_on'
    list_filter = ('published', 'content_format')
    search_fields = ('title', 'raw_content', 'tag_string')
    prepopulated_fields = {"slug": ("title", )}
    actions = ['publish_entries']

    def publish_entries(self, request, queryset):
        for entry in queryset:
            entry.publish()

admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Entry, EntryAdmin)
