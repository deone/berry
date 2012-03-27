from django import forms
from django.shortcuts import render_to_response, get_object_or_404

from accounts.models import SubscriberInfo
from refer.models import Member

import datetime
import random
import string


class ReferrerNumberForm(forms.Form):
    phone_number = forms.CharField(label="Referrer's Number", max_length=11)

    def save(self, request):
	request.session['referrer'] = self.cleaned_data['phone_number']

	subscriber = get_object_or_404(SubscriberInfo,
		msisdn=self.cleaned_data['phone_number'])

	return subscriber


class UserNumberForm(forms.Form):
    phone_number = forms.CharField(label="Your Number", max_length=11)

    def save(self, request):
	subscriber = get_object_or_404(SubscriberInfo,
		msisdn=request.session['referrer'])
	referrer, created = Member.objects.get_or_create(
		subscriber=subscriber,
		)

	member = referrer

	request.session.flush()
	raw_password = "".join(random.sample('%s%s' % (string.lowercase, string.digits), 6))

	if member.member_referrer.count() % 2 == 0:
	    # Step through downlines continuing if downline has a downline
	    while member.left is not None:
		member = member.left
		continue

	    subscriber = get_object_or_404(SubscriberInfo,
		    msisdn=self.cleaned_data['phone_number'])

	    member.left = Member.objects.create(subscriber=subscriber, referrer=referrer)
	    new_member = member.left

	else:
	    while member.right is not None:
		member = member.right
		continue

	    subscriber = get_object_or_404(SubscriberInfo,
		    msisdn=self.cleaned_data['phone_number'])

	    member.right = Member.objects.create(subscriber=subscriber, referrer=referrer)
	    new_member = member.right

	new_member.set_password(raw_password)
	new_member.save()

	referrer.latest_update_at = datetime.datetime.now()
	referrer.save()

	return new_member, raw_password
