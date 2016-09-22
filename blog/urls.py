# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # /blog/ | /
    url(r'^$', views.article_list_view, name='blog.article_list'),
]