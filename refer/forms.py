from django import forms
from django.shortcuts import render_to_response, get_object_or_404

from accounts.models import SubscriberInfo

class ReferrerNumberForm(forms.Form):
    phone_number = forms.CharField(label="Referrer's Number", max_length=11)

    def save(self):
	subscriber = get_object_or_404(SubscriberInfo,
		msisdn=self.cleaned_data['phone_number'])

	return subscriber
