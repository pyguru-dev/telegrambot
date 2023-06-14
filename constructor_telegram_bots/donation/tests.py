from django import urls

from constructor_telegram_bots.tests import BaseTestCase


class DonationViewsTest(BaseTestCase):
	def test_donation_view(self) -> None:
		self.assertTemplateUsed(
			url=urls.reverse('donation'),
			template_name='donation.html'
		)
