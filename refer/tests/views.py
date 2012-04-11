from django.test import TestCase
from django.core.urlresolvers import reverse

class ReferViewsTestCase(TestCase):

    fixtures = ['usertestdata.json', 'subscriberinfotestdata.json']

    def setUp(self):
	self.client.get(reverse('join_pre'))
	s = self.client.session
	s['testcookie'] = 'worked'
	s.save()

    def test_get_pre_join(self):
	response = self.client.get(reverse('join_pre'))
	self.assertEqual(response.status_code, 200)
	self.assertTrue('form' in response.context)

    def test_post_pre_join(self):
	data = {
		'phone_number': '08051111111'
		}
	response = self.client.post(reverse('join_pre'), data)
	self.assertTrue('subscriber' in response.context)
	self.assertTrue('form' in response.context)
	self.assertEqual(response.status_code, 200)
