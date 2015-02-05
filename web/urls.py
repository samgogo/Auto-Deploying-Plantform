#coding=utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from first.views import *

#from first.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
       (r'^$', index),
       (r'^serverscreate.html/$', serverscreate),
       (r'^serversdelete/$', serversdelete),
       (r'^serversclear/$', serversclear),
       (r'^serversverify/$', serversverify),
       (r'^serversinstall/$', serversinstall),
)