from django import forms
from django.forms.util import ErrorList
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode

from accounts.models import SubscriberInfo
from refer.models import Member, Rank

import datetime
import random
import string


class ReferrerNumberForm(forms.Form):
    phone_number = forms.CharField(label="Referrer's Number",
	    widget=forms.TextInput(attrs={'class': 'integer input-large',
		'placeholder': "Referrer's Number"}), max_length=11)

    def clean_phone_number(self):
	msisdn_prefix = self.cleaned_data['phone_number'][:4]
	if msisdn_prefix not in settings.MSISDN_PREFIXES:
	    raise forms.ValidationError("This phone number is not valid.")
	self.cleaned_data['phone_number'] = "+234" + self.cleaned_data['phone_number'][1:]

	return self.cleaned_data['phone_number']


class UserNumberForm(ReferrerNumberForm):
    def __init__(self, *args, **kwargs):
	super(UserNumberForm, self).__init__(*args, **kwargs)
	self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'integer input-large',
	    'placeholder': "Your Number", 'maxlength': 11})

    def clean_phone_number(self):
	intl_phone_no = "+234" + self.cleaned_data['phone_number'][1:]

	registered_sub_nos = [str(m.subscriber.msisdn) for m in Member.objects.all()]
	if intl_phone_no in registered_sub_nos:
	    raise forms.ValidationError("""This subscriber is already registered as a member.""")

	super(UserNumberForm, self).clean_phone_number()
	return self.cleaned_data['phone_number']

    def save(self, referrer_no, referral_no):
	referrer_subscriber = get_object_or_404(SubscriberInfo,
		msisdn=referrer_no)
	referral_subscriber = get_object_or_404(SubscriberInfo,
		msisdn=referral_no)

	# Get referrer or create if he doesn't already exist.
	referrer, created = Member.objects.get_or_create(subscriber=referrer_subscriber)

	parent = get_parent(referrer)

	# Create referral model instance, also set rank to 0.
	referral = Member.objects.create(subscriber=referral_subscriber, referrer=referrer, parent=parent)
	referral_password = set_password(referral)
	set_rank(referral)

	if created:
	    referrer_password = set_password(referrer)
	    set_rank(referrer)
	else:
	    referrer_password = None
	    
	notify(referrer, 'referrer', referrer_password, created)
	notify(referral, 'referral', referral_password)

	return referrer, referral

def get_parent(referrer):
    if referrer.get_children().count() < 2:
	return referrer
    else:
	descendants = referrer.get_descendants()
	leaf_node_ids = [m.id for m in descendants if m.is_leaf_node()]
	return descendants.get(pk=min(leaf_node_ids))

    # TODO 1
    # descendants = referrer.get_descendants(True)
    # node_ids = [m.id for m in descendants if m.get_children().count() < 2]
    # return descendants.get(pk=min(node_ids))

def set_rank(member):
    Rank.objects.create(member=member, rank=0)

def set_password(member):
    raw_password = "".join(random.sample('%s%s' % (string.lowercase, string.digits), 6))
    member.subscriber.user.set_password(raw_password)
    member.subscriber.user.save()

    return raw_password

def notify(member, mtype, password, created=False):
    subject = "Your Freebird Reward System Account"
    message = """Thank you for joining the Freebird Reward System.
	    You may log in to the web site with the following credentials:
	    Username: %s
	    Password: %s

	    Cheers!
	    """ % (member.subscriber.get_msisdn(), password)

    if mtype == 'referrer':
	if created:
	    message = message + """P.S: You were automatically registered as a 
	    result of the registration of your first 
	    referree, %s""" % member.referrals.all()[0].subscriber.user.get_full_name()
	else:
	    subject = "New Referral in your Freebird Reward System Account"
	    message = "You have a new referral in your network."
    else:
	pass

    member.subscriber.user.email_user(subject, message, settings.SENDER_EMAIL)


class DivErrorList(ErrorList):
    def __unicode__(self):
	return self.as_divs()
    def as_divs(self):
	if not self:
	    return u''
	return mark_safe(u'<div class="errorlist">%s</div>'
                % ''.join([u"""
		<div class="alert alert-error fade in">
		    <button class="close" data-dismiss="alert">&times;</button>%s
		</div>""" % conditional_escape(force_unicode(e)) for e in self]))
