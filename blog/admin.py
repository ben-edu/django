# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Article, Tag
# Register your models here.

admin.site.register(Article)
admin.site.register(Tag)

class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title', 'owner', 'create_at',)

admin.site.unregister(Article)
admin.site.register(Article, ArticleAdmin)