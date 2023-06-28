from django.test import TestCase, Client
from django import urls


class UpdatesViewsTest(TestCase):
	def setUp(self) -> None:
		self.client = Client(enforce_csrf_checks=True)

	def test_team_view(self) -> None:
		response = self.client.get(urls.reverse('updates'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'updates.html')
