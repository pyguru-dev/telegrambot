from django import urls

from constructor_telegram_bots.tests import BaseTestCase


class PrivacyPolicyViewsTest(BaseTestCase):
	def test_privacy_policy_view(self) -> None:
		self.assertTemplateUsed(
			url=urls.reverse('privacy_policy'),
			template_name='privacy_policy.html'
		)
