from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver

from refer.forms import ReferrerNumberForm, UserNumberForm
from accounts.models import SubscriberInfo
from refer.models import Member

def index(request, template='refer/index.html', form=ReferrerNumberForm):
    context = {}
    if request.method == "POST":
	if request.session.test_cookie_worked():
	    request.session.delete_test_cookie()
	else:
	    return HttpResponse("Please enable cookies and try again.")

	form = form(request.POST)
	if form.is_valid():
	    request.session['referrer'] = form.cleaned_data['phone_number']
	    subscriber = get_object_or_404(SubscriberInfo,
		msisdn=form.cleaned_data['phone_number'])
	    context['subscriber'] = subscriber

    else:
	form = form()

    context['form'] = form
    request.session.set_test_cookie()

    return render_to_response(template, context, context_instance=RequestContext(request))

def join_final(request, template='refer/final.html', form=UserNumberForm):
    context = {}
    if request.method == "POST":
	form = form(request.POST)
	if form.is_valid():
	    request.session['referree'] = form.cleaned_data['phone_number']
	    subscriber = get_object_or_404(SubscriberInfo,
		msisdn=form.cleaned_data['phone_number'])
	    context['subscriber'] = subscriber
    else:
	form = form()

    context['form'] = form
    return render_to_response(template, context, context_instance=RequestContext(request))

def join_done(request, form=UserNumberForm):
    if request.session.get('referrer') and request.session.get('referree'):
	referrer, referree = request.session['referrer'], request.session['referree']
	form = form()
	member = form.save(referrer, referree)

	request.session.flush()

	return HttpResponse("""%s, thank you for joining the Freebird Reward
	    System. Notifications have been sent to your email address and
	    phone.""" % member.subscriber.user.get_full_name())
    else:
	return HttpResponse("Please commence your registration <a href='%s'>here</a>." %
		reverse('join_pre'))

@receiver(post_save, sender=Member)
def check_eligibility(sender, instance, **kwargs):
    """
    We need to traverse the tree everytime a new member is added, and apportion
    some form of points or note their states.
    Modified Pre-order Tree Traversal might be the secret to this.
    """
    if kwargs['created']:
	pass
