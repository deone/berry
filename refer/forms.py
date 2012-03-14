from django import forms
from django.shortcuts import render_to_response, get_object_or_404

from accounts.models import SubscriberInfo

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
	# Do all you want to do.
	request.session.flush()
