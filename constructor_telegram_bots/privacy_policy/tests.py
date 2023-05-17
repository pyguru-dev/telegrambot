from django.test import TestCase, Client


class PrivacyPolicyViewsTest(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

	def test_privacy_policy_view(self) -> None:
		response = self.client.get('/privacy-policy/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'privacy_policy.html')
