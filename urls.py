from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import os

urlpatterns = patterns('',
    (r'^', include('accounts.urls')),
    url(r'^join/pre$', 'refer.views.index', name='join_pre'),
    url(r'^join/final$', 'refer.views.join_final', name='join_final'),
    url(r'^join/done$', 'refer.views.join_done', name='join_done'),
    (r'^members$', 'refer.views.show_members'),
    (r'^genres/$', 'myapp.views.show_genres'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': settings.MEDIA_ROOT}),
)
