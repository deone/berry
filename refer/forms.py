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


class UserNumberForm(ReferrerNumberForm):
    def __init__(self, *args, **kwargs):
	super(UserNumberForm, self).__init__(*args, **kwargs)
	self.fields['phone_number'].label = "Your Number"

    def clean(self):
	intl_phone_no = "+234" + self.cleaned_data['phone_number'][1:]

	registered_sub_nos = [str(m.subscriber.msisdn) for m in Member.objects.all()]
	if intl_phone_no in registered_sub_nos:
	    raise forms.ValidationError("""This subscriber is already registered as a member.""")

	super(UserNumberForm, self).clean()
	return self.cleaned_data

    def save(self, referrer_no, referral_no):
	referrer_subscriber = get_object_or_404(SubscriberInfo,
		msisdn=referrer_no)
	referral_subscriber = get_object_or_404(SubscriberInfo,
		msisdn=referral_no)

	# Get referrer or create if he doesn't already exist.
	referrer, created = Member.objects.get_or_create(subscriber=referrer_subscriber)

	# Get parent - earliest added leaf node of referrer.
	if len(referrer.get_leafnodes()) < settings.MAX_CHILDREN:
	    parent = referrer
	else:
	    leaf_node_ids = [m.id for m in referrer.get_leafnodes()]
	    parent = referrer.get_leafnodes().get(pk=min(leaf_node_ids))

	# Create referral model instance.
	referral = Member.objects.create(subscriber=referral_subscriber, referrer=referrer, parent=parent)

	# Set referral password and save.
	referral_raw_password = "".join(random.sample('%s%s' % (string.lowercase, string.digits), 6))
	referral.subscriber.user.set_password(referral_raw_password)
	referral.subscriber.user.save()

	# Send notifications to referrer and referral.
	# If referrer is new, send him a welcome email.
	if created:
	    referrer_raw_password = "".join(random.sample('%s%s' % (string.lowercase, string.digits), 6))
	    referrer.subscriber.user.set_password(referrer_raw_password)
	    referrer.subscriber.user.save()
	    referrer.subscriber.user.email_user("Your Freebird Reward System Account", 
		"""Thank you for joining the Freebird Reward System. You were
		automatically registered as a result of the registration of your
		first referree, %s
		You may log in to the web site with the following credentials:
		Username: %s
		Password: %s

		Cheers!
		""" % (referral.subscriber.user.get_full_name(),
		    referrer.subscriber.get_msisdn(), referrer_raw_password),
		settings.SENDER_EMAIL)
	else:
	    referrer.subscriber.user.email_user("New Referree in your Freebird Reward System Account", 
		    "You have a new referree in your network.",
		    settings.SENDER_EMAIL)

	# Update referrer with timestamp - to be able to track last activity.
	referrer.latest_update_at = datetime.datetime.now()
	referrer.save()

	referral.subscriber.user.email_user("Your Freebird Reward System Account", 
		"""Thank you for joining the Freebird Reward System.
		You may log in to the web site with the following credentials:
		Username: %s
		Password: %s

		Cheers!
		""" % (referral.subscriber.get_msisdn(), referral_raw_password),
		settings.SENDER_EMAIL)

	return referrer, referral
