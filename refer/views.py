from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from refer.forms import *
from refer.models import Member
from accounts.models import *

from datetime import datetime


def show_members(request, template='refer/members.html'):
    count = {}
    for member in Member.objects.all():
	if member.is_leaf_node():
	    left, right = 0, 0
	elif len(member.get_children()) == 1:
	    left, right = int(member.get_children()[0].get_descendant_count() +
		    1), 0
	else:
	    children = member.get_children()
	    left = int(children[0].get_descendant_count() + 1)
	    right = int(children[1].get_descendant_count() + 1)

	left_right = [left, right]
	count[member] = left_right

    return render_to_response(
	    template,
	    {
		'members': Member.objects.all(),
		'descendant_count': count
		},
	    context_instance=RequestContext(request))

def index(request, template='refer/index.html', form=ReferrerNumberForm):
    context = {}
    if request.method == "POST":
	if request.session.test_cookie_worked():
	    request.session.delete_test_cookie()
	else:
	    return HttpResponse("Please enable cookies and try again.")

	form = form(request.POST, error_class=DivErrorList)
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
	form = form(request.POST, error_class=DivErrorList)
	if form.is_valid():
	    request.session['referral'] = form.cleaned_data['phone_number']
	    subscriber = get_object_or_404(SubscriberInfo,
		msisdn=form.cleaned_data['phone_number'])
	    context['subscriber'] = subscriber
    else:
	form = form()

    context['form'] = form
    return render_to_response(template, context, context_instance=RequestContext(request))

def join_done(request, template="feedback.html", form=UserNumberForm):
    try:
	referrer, referral = request.session['referrer'], request.session['referral']
    except KeyError, e:
	return render_to_response(template, {}, context_instance=RequestContext(request))
    else:
	form = form()
	referrer, referral = form.save(referrer, referral)

	request.session.flush()

	return render_to_response(template, {'user': referral.subscriber.user}, context_instance=RequestContext(request))

@receiver(post_save, sender=Member)
def pay_bonus(sender, instance, **kwargs):
    member = instance.referrer
    if member:
	if member.is_standard():
	    RefillHistory.objects.create(subscriber=member.subscriber,
		    last_recharge_amount=settings.BONUS_PER_REFERRAL * 2, source="GLPRB")

	elif member.is_bronze():
	    RefillHistory.objects.create(subscriber=member.subscriber,
		    last_recharge_amount=settings.BONUS_PER_REFERRAL * 4, source="GLPRB")

	elif member.is_silver():
	    RefillHistory.objects.create(subscriber=member.subscriber,
		    last_recharge_amount=settings.BONUS_PER_REFERRAL * 8, source="GLPRB")

	elif member.is_gold():
	    RefillHistory.objects.create(subscriber=member.subscriber,
		    last_recharge_amount=settings.BONUS_PER_REFERRAL * 16, source="GLPRB")

	elif member.is_platinum():
	    RefillHistory.objects.create(subscriber=member.subscriber,
		    last_recharge_amount=settings.BONUS_PER_REFERRAL * 32, source="GLPRB")

	elif member.is_diamond():
	    RefillHistory.objects.create(subscriber=member.subscriber,
		    last_recharge_amount=settings.BONUS_PER_REFERRAL * 64, source="GLPRB")

	else:
	    pass
