from django.test import TestCase
from django.core import mail

from refer.forms import *

from datetime import datetime

class ReferrerNumberFormTestCase(TestCase):

	def test_invalid_number(self):
	    data = {
		'phone_number': '08022334455'
		}
	    form = ReferrerNumberForm(data)
	    self.assertFalse(form.is_valid())
	    self.assertEqual(form.errors['__all__'],
		    [u'This phone number is not valid.'])


class UserNumberFormTestCase(ReferrerNumberFormTestCase):
    
    fixtures = ['usertestdata.json', 'subscriberinfotestdata.json', 'membertestdata.json']

    def test_field_label(self):
	form = UserNumberForm()
	self.assertEqual(form.fields['phone_number'].label, "Your Number")

    def test_existing_member(self):
	data = {
		'phone_number': '08051111111'
		}
	form = UserNumberForm(data)
	self.assertFalse(form.is_valid())
	self.assertEqual(form.errors['__all__'], [u"""This subscriber is already registered as a member."""])

    def test_success(self):
	rf, rfrl = "+2348050666666", "+2348050444444"
	form = UserNumberForm()
	r, m = form.save(rf, rfrl)
	self.assertEqual(len(mail.outbox), 2)
	self.assertEqual(repr(m), "<Member: +2348050444444>")
	# Check whether referrer is newly created.
	self.assertEqual(r.date_joined.second, datetime.now().second)
	self.assertEqual(m.date_joined.second, r.latest_update_at.second)
