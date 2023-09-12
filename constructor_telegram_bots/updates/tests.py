from django.test import TestCase
from django.http import HttpResponse
from django import urls

from .models import Update


class UpdateModelTests(TestCase):
	def setUp(self) -> None:
		self.update = Update.objects.create(version='0.0.0-beta', description='None...')

	def test_fields(self) -> None:
		self.assertEqual(str(self.update.image), '')
		self.assertEqual(self.update.version, '0.0.0-beta')
		self.assertEqual(self.update.description, 'None...')
		self.assertIsNotNone(self.update.added_date)

class ViewsTests(TestCase):
	def test_updates_view(self) -> None:
		url: str = urls.reverse('updates')
		response: HttpResponse = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'updates.html')

	def test_update_view(self) -> None:
		url: str = urls.reverse('update', kwargs={'update_id': 1})

		response: HttpResponse = self.client.get(url)
		self.assertJSONEqual(response.content, {
			'message': 'Обновление не найдено!',
			'level': 'danger',
		})

		Update.objects.create(version='0.0.0-beta', description='None...')

		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'update.html')
