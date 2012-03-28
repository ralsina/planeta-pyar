# -*- coding: utf-8 *-*

from django.contrib import admin
from models import Feed


class FeedAdmin(admin.ModelAdmin):

    fields = ('author', 'url_feed', 'interval', 'python_feed', 'global_feed')
    list_filter = ('author', 'url_feed', 'python_feed', 'global_feed')


admin.site.register(Feed, FeedAdmin)
