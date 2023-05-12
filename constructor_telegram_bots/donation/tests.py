from django.test import TestCase, Client


class DonationViewsTest(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

	def test_donation_view(self) -> None:
		response = self.client.get('/donation/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'donation.html')
