from django.test import TestCase
from django.http import HttpResponse
from django import urls

from .models import Donation

from datetime import datetime


class DonationModelTests(TestCase):
	def setUp(self) -> None:
		self.current_date: datetime = datetime.now()
		self.donation: Donation = Donation.objects.create(sum=50.00, telegram_url='https://example.com/', date=self.current_date)

	def test_fields(self) -> None:
		self.assertEqual(self.donation.sum, 50.00)
		self.assertEqual(self.donation.telegram_url, 'https://example.com/')
		self.assertEqual(self.donation.date, self.current_date)

class ViewsTests(TestCase):
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
