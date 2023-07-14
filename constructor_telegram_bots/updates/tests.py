from constructor_telegram_bots.tests import BaseTestCase

from django.http import HttpResponse
from django import urls

from .models import Update


class UpdatesViewsTest(BaseTestCase):
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

		Update.objects.create(title='test', description='test')

		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'update.html')
