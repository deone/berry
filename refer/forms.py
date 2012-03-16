from django import forms
from django.shortcuts import render_to_response, get_object_or_404

from accounts.models import SubscriberInfo
from refer.models import Member

import datetime

POSITION_CHOICES = (
	("", "Select Position"),
	("L", "Left"),
	("R", "Right"),
)

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
	referrer, created = Member.objects.get_or_create(
		phone_number=request.session['referrer'],
		)

	member = referrer

	if member.member_referrer.count() % 2 == 0:
	    # Step through downlines continuing if downline has a downline
	    while member.left is not None:
		member = member.left
		continue

	    # We finally have the last downline who doesn't have a downline in the
	    # specified position. And we create one.
	    member.left = create_member(referrer,
		    self.cleaned_data['phone_number'])
	else:
	    while member.right is not None:
		member = member.right
		continue

	    member.right = create_member(referrer,
		    self.cleaned_data['phone_number'])

	member.save()

	request.session.flush()

	referrer.latest_update_at = datetime.datetime.now()
	referrer.save()

	return referrer

def create_member(referrer, phone_number):
    return Member.objects.create(referrer=referrer, phone_number=phone_number)
