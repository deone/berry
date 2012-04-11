from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from accounts.models import SubscriberInfo

PICTURE_LOCATION = '/home/deone/Pictures/Me/20110625_003b.jpg'

class SubscriberInfoTestCase(TestCase):
    fixtures = ['usertestdata.json']

    def setUp(self):
	self.user = get_object_or_404(User, pk=5)
	photo = open(PICTURE_LOCATION, 'rb')
	self.photo = SimpleUploadedFile(photo.name, photo.read())

    def test_success(self):
	s = SubscriberInfo.objects.create(user=self.user,
		msisdn="+2348051111111", photo=self.photo)
	self.assertEqual(repr(s), '<SubscriberInfo: +2348051111111>')

    def test_get_msisdn(self):
	s = SubscriberInfo.objects.create(user=self.user, msisdn="+2348051111111",
		photo=self.photo)
	self.assertTrue(s.get_msisdn().startswith("0805"))
