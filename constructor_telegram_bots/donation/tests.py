from django.test import TestCase, Client
from django.http import HttpResponse
from django import urls


class DonationViewsTests(TestCase):
	def setUp(self) -> None:
		self.client = Client()

	def test_donation_view(self) -> None:
		url: str = urls.reverse('donation')
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'donation.html')

	def test_donation_completed_view(self) -> None:
		url: str = urls.reverse('donation_completed')
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'donation_completed.html')
