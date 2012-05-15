from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.contrib import auth

def index(request, template="accounts/index.html"):
    return render_to_response(template, {},
	    context_instance=RequestContext(request))

def logout(request):
    auth.logout(request)
    return redirect(reverse('signin'))
