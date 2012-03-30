from django.test import TestCase
from django.shortcuts import get_object_or_404

from accounts.models import SubscriberInfo
from refer.models import *

class MemberModelTestCase(TestCase):
    fixtures = ['authtestdata.json', 'accountstestdata.json']

    def setUp(self):
	referrer_subscriber = get_object_or_404(SubscriberInfo, pk=1)
	self.referrer = Member.objects.create(subscriber=referrer_subscriber)

    def test_create_referrer(self):
	self.assertEqual(self.referrer.referrer, None)
	self.assertEqual(repr(self.referrer), '<Member: 08051111111>')
	self.assertEqual(self.referrer.password, "")
	self.assertEqual(self.referrer.right, None)
	self.assertEqual(self.referrer.left, None)

    def test_create_referree(self):
	referree_subscriber = get_object_or_404(SubscriberInfo, pk=2)
	self.referrer.left = Member.objects.create(
		referrer = self.referrer, 
		subscriber=referree_subscriber)
	self.referree = self.referrer.left

	self.assertEqual(repr(self.referree), '<Member: 08052222222>')
	self.assertEqual(self.referree.referrer, self.referrer)
