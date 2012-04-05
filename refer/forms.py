from django import forms
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings

from accounts.models import SubscriberInfo
from refer.models import Member

import datetime
import random
import string


class ReferrerNumberForm(forms.Form):
    phone_number = forms.CharField(label="Referrer's Number",
	    widget=forms.TextInput(attrs={'class': 'integer'}), max_length=11)

    def clean(self):
	msisdn_prefix = self.cleaned_data['phone_number'][:4]
	if msisdn_prefix not in settings.MSISDN_PREFIXES:
	    raise forms.ValidationError("This phone number is not valid.")
	self.cleaned_data['phone_number'] = "+234" + self.cleaned_data['phone_number'][1:]

	return self.cleaned_data

    def save(self, request):
	request.session['referrer'] = self.cleaned_data['phone_number']

	subscriber = get_object_or_404(SubscriberInfo,
		msisdn=self.cleaned_data['phone_number'])

	return subscriber


class UserNumberForm(ReferrerNumberForm):
    def __init__(self, *args, **kwargs):
	super(UserNumberForm, self).__init__(*args, **kwargs)
	self.fields['phone_number'].label = "Your Number"

    def clean(self):
	intl_phone_no = "+234" + self.cleaned_data['phone_number'][1:]

	registered_sub_nos = [str(m.subscriber.msisdn) for m in Member.objects.all()]
	if intl_phone_no in registered_sub_nos:
	    raise forms.ValidationError("Error!")

	super(UserNumberForm, self).clean()
	return self.cleaned_data

    def _create_referree(self, referree):
	subscriber = get_object_or_404(SubscriberInfo,
		msisdn=referree)
	if self.position == 'right':
	    self.member_above.right = Member.objects.create(subscriber=subscriber,
		referrer=self.referrer)
	    self.member_above.save()
	    return self.member_above.right
	else:
	    self.member_above.left = Member.objects.create(
		subscriber=subscriber, 
		referrer=self.referrer)
	    self.member_above.save()
	    return self.member_above.left

    def _get_member_above(self):
	""" Get member to position referree under """
	member = self.referrer
	if member.member_referrer.count() % 2 == 0:
	    while member.left is not None:
		member = member.left
		continue
	    return "left", member
	else:
	    while member.right is not None:
		member = member.right
		continue
	    return "right", member

    def _set_password(self, _type):
	raw_password = "".join(random.sample('%s%s' % (string.lowercase, string.digits), 6))
	if _type == "member":
	    self.member.set_password(raw_password)
	    self.member.save()
	else:
	    self.referrer.set_password(raw_password)
	    self.referrer.save()
	return raw_password

    def _get_or_create_referrer(self, subscriber):
	return Member.objects.get_or_create(subscriber=subscriber)

    def check_referree(self, request):
	request.session['referree'] = self.cleaned_data['phone_number']

	subscriber = get_object_or_404(SubscriberInfo,
		msisdn=self.cleaned_data['phone_number'])

	return subscriber

    def save(self, request):
	subscriber = get_object_or_404(SubscriberInfo,
		msisdn=request.session['referrer'])

	self.referrer, self.created = self._get_or_create_referrer(subscriber)
	self.position, self.member_above = self._get_member_above()
	self.member = self._create_referree(request.session['referree'])
	member_password = self._set_password("member")

	self.referrer.latest_update_at = datetime.datetime.now()
	self.referrer.save()

	if self.created:
	    referrer_password = self._set_password("referrer")
	    self.referrer.subscriber.user.email_user("Your Freebird Reward System Account", 
		"""Thank you for joining the Freebird Reward System. You were
		automatically registered as a result of the registration of your
		first referree, %s
		You may log in to the web site with the following credentials:
		Username: %s
		Password: %s

		Cheers!
		""" % (self.member.subscriber.user.get_full_name(),
		    self.referrer.subscriber.get_msisdn(), referrer_password),
		settings.SENDER_EMAIL)

	self.member.subscriber.user.email_user("Your Freebird Reward System Account", 
		"""Thank you for joining the Freebird Reward System.
		You may log in to the web site with the following credentials:
		Username: %s
		Password: %s

		Cheers!
		""" % (self.member.subscriber.get_msisdn(), member_password),
		settings.SENDER_EMAIL)

	self.referrer.subscriber.user.email_user("New Referree in your Freebird Reward System Account", 
		"""You have a new referree in your network.""",
		settings.SENDER_EMAIL)

	request.session.flush()

	return self.member
