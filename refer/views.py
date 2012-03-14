from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from refer.forms import ReferrerNumberForm

def index(request, template='refer/index.html', form=ReferrerNumberForm):
    context = {}
    if request.method == "POST":
	form = form(request.POST)
	if form.is_valid():
	    subscriber = form.save()
	    context['referrer'] = subscriber

    else:
	form = form()

    context['form'] = form

    return render_to_response(template, context, context_instance=RequestContext(request))
