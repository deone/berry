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


class PositionForm(forms.Form):
    position = forms.ChoiceField(choices=POSITION_CHOICES,
	    widget=forms.Select())

    def save(self, request):
	request.session['position'] = self.cleaned_data['position']


class UserNumberForm(forms.Form):
    phone_number = forms.CharField(label="Your Number", max_length=11)

    def save(self, request):
	referrer, created = Member.objects.get_or_create(
		phone_number=request.session['referrer'],
		)

	member = referrer

	if request.session['position'] == "L":
	    while member.left is not None:
		member = member.left
		continue

	    member.left = Member.objects.create(
		    referrer=referrer,
		    phone_number=self.cleaned_data['phone_number']
		    )
	else:
	    while member.right is not None:
		member = member.right
		continue

	    member.right = Member.objects.create(
		    referrer=referrer,
		    phone_number=self.cleaned_data['phone_number']
		    )

	member.save()

	request.session.flush()

	referrer.latest_update_at = datetime.datetime.now()
	referrer.save()

	return referrer

def count_downlines(member, position):
    count = 0

    if position.lower() == "left":
	while member.left is not None:
	    count += 1
	    continue

    return count + 1
