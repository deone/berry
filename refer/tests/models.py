from django.test import TestCase
from django.shortcuts import get_object_or_404

from accounts.models import SubscriberInfo
from refer.models import *

class MemberTestCase(TestCase):

    fixtures = ['usertestdata.json', 'subscriberinfotestdata.json']

    def setUp(self):
	subscriber = get_object_or_404(SubscriberInfo, pk=9)
	self.referrer = Member.objects.create(subscriber=subscriber)

    def test_create_referrer(self):
	self.assertEqual(repr(self.referrer), '<Member: +2348050999999>')
	self.assertEqual(self.referrer.parent, None)

    def test_create_referral(self):
	rs = get_object_or_404(SubscriberInfo, pk=10)
	rfrl = Member.objects.create(subscriber=rs, parent=self.referrer)

	self.assertEqual(repr(rfrl), '<Member: +2348050000000>')
	self.assertEqual(rfrl.parent, self.referrer)
