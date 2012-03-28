from django.conf.urls import patterns, include, url
from django.contrib import admin
from feeds import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_planeta_pyar.views.home', name='home'),
    # url(r'^django_planeta_pyar/', include('django_planeta_pyar.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^globalfeeds/', views.get_global_feeds),
    url(r'^pythonfeeds/', views.get_python_feeds),
)
