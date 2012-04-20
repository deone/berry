from django.test import TestCase
from django.core.urlresolvers import reverse


class ReferViewsTestCase(TestCase):

    fixtures = ['usertestdata.json', 'subscriberinfotestdata.json']

    def setUp(self):
	self.client.get(reverse('join_pre'))

    def test_get_pre_join(self):
	response = self.client.get(reverse('join_pre'))
	self.assertEqual(response.status_code, 200)
	self.assertTrue('form' in response.context)
	self.assertTrue(response.templates[0].name, 'refer/index.html')
	self.assertTrue(response.templates[1].name, 'base.html')

    def test_post_pre_join(self):
	data = {
		'phone_number': '08051111111'
		}
	response = self.client.post(reverse('join_pre'), data)
	self.assertTrue(response.templates[0].name, 'refer/index.html')
	self.assertTrue(response.templates[1].name, 'base.html')
	self.assertTrue('subscriber' in response.context)
	self.assertEqual(response.context['subscriber'].user.get_full_name(), "K K")
	self.assertTrue('form' in response.context)
	self.assertEqual(response.status_code, 200)

    def test_get_join_final(self):
	response = self.client.get(reverse('join_final'))
	self.assertEqual(response.status_code, 200)
	self.assertTrue('form' in response.context)
	self.assertTrue(response.templates[0].name, 'refer/final.html')
	self.assertTrue(response.templates[1].name, 'base.html')

    def test_post_join_final(self):
	data = {
		'phone_number': '08051111111'
		}
	response = self.client.post(reverse('join_final'), data)
	self.assertTrue(response.templates[0].name, 'refer/final.html')
	self.assertTrue(response.templates[1].name, 'base.html')
	self.assertEqual(response.context['subscriber'].user.get_full_name(), "K K")
	self.assertTrue('subscriber' in response.context)
	self.assertTrue('form' in response.context)
	self.assertEqual(response.status_code, 200)

    def test_join_done(self):
	s = self.client.session
	s['referrer'] = '+2348051111111'
	s['referral'] = '+2348051222222'
	s.save()
	response = self.client.get(reverse('join_done'))
	self.assertContains(response, "L L, thank you for joining the Freebird")

    def test_join_done_invalid_session(self):
	response = self.client.get(reverse('join_done'))
	self.assertContains(response, "Please commence your registration")

    def tearDown(self):
	self.client.session.flush()
