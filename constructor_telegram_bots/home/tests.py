from django.test import TestCase, Client
from django import urls


class HomeViewsTest(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

	def test_home_view(self) -> None:
		response = self.client.get(urls.reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
