from django.test import TestCase, Client
from django.http import HttpResponse
from django import urls


class PrivacyPolicyViewsTests(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

	def test_privacy_policy_view(self) -> None:
		response: HttpResponse = self.client.get(urls.reverse('privacy_policy'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'privacy_policy.html')
