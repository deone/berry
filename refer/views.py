from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from refer.forms import ReferrerNumberForm, UserNumberForm
from accounts.models import SubscriberInfo

def index(request, template='refer/index.html', form=ReferrerNumberForm):
    context = {}
    if request.method == "POST":
	
	if request.session.test_cookie_worked():
	    request.session.delete_test_cookie()
	else:
	    return HttpResponse("Please enable cookies and try again.")

	form = form(request.POST)
	if form.is_valid():
	    subscriber = form.save(request)
	    context['referrer'] = subscriber

    else:
	form = form()

    context['form'] = form
    request.session.set_test_cookie()

    return render_to_response(template, context, context_instance=RequestContext(request))

def join_final(request, template='refer/final.html', form=UserNumberForm):
    if request.method == "POST":
	form = form(request.POST)
	if form.is_valid():
	    result = form.save(request)
	    if result:
		pass	# send email/sms
	    return HttpResponse("""Thank you for joining the Freebird Reward
	    System""")
    else:
	form = form()

    return render_to_response(template, {'form': form}, context_instance=RequestContext(request))
