from django.conf.urls.defaults import *

from accounts.forms import AuthForm

urlpatterns = patterns('accounts.views',
    url(r'^home$', 'index', name='join'),
    url(r'^signout$', 'logout', name='signout'),
)

urlpatterns += patterns('',
    url(r'^signin$', 'django.contrib.auth.views.login', {'template_name':
	'accounts/login.html', 'authentication_form': AuthForm}, 'signin'),
)
