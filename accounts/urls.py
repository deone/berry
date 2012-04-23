from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    url(r'^home$', 'index', name='join'),
    url(r'^logout$', 'logout', name='logout'),
)

urlpatterns += patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':
	'accounts/login.html'}, 'login'),
)
