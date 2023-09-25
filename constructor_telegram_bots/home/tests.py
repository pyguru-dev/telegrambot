from django.test import TestCase
from django.http import HttpResponse
from django import urls


class ViewsTests(TestCase):
	def test_home_view(self) -> None:
		url: str = urls.reverse('home')
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
