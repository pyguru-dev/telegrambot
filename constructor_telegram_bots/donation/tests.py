from django.test import TestCase, Client
from django.http import HttpResponse
from django import urls


class DonationViewsTests(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

	def test_donation_view(self) -> None:
		response: HttpResponse = self.client.get(urls.reverse('donation'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'donation.html')

	def test_donation_completed_view(self) -> None:
		response: HttpResponse = self.client.get(urls.reverse('donation_completed'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'donation_completed.html')