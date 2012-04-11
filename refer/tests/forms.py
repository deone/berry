from django.test import TestCase
from django.core import mail

from refer.forms import *

class ReferrerNumberFormTestCase(TestCase):

	def test_valid_number(self):
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
	referrer, referree = "+2348053333333", "+2348054444444"
	form = UserNumberForm()
	m = form.save(referrer, referree)
	self.assertEqual(repr(form.referrer), "<Member: +2348053333333>")
	self.assertTrue(repr(form.referrer_created))
	self.assertEqual(len(mail.outbox), 3)
	self.assertEqual(repr(m), "<Member: +2348054444444>")
