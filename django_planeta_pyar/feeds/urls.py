# -*- coding: utf-8 *-*

from django.conf.urls.defaults import *
from feeds import views


urlpatterns = patterns('',
    url(r'^/globalfeeds$', views.get_global_feeds),
    url(r'^/pythonfeeds$', views.get_python_feeds),
)
